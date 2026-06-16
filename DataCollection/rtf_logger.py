import rclpy
from rclpy.node import Node
from rosgraph_msgs.msg import Clock
import time
import csv

class RTFLogger(Node):
    def __init__(self):
        super().__init__('rtf_logger')
        
        # Ne abonăm la clock, dar salvăm doar valoarea în memorie (fără procesare grea aici)
        self.subscription = self.create_subscription(Clock, '/clock', self.clock_callback, 10)
        
        # Deschidem fișierul direct cu buffering=1 (scrie linie cu linie, nu pierde date)
        self.csv_file = open('rtf_log.csv', mode='w', newline='', encoding='utf-8', buffering=1)
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['Sim_Time_Sec', 'Real_Time_Sec', 'Instantaneous_RTF'])
        
        self.current_sim_time = 0.0
        self.last_sim_time = None
        self.last_real_time = None
        
        # Pornim un timer care rulează EXCLUSIV o dată pe secundă (1Hz)
        self.timer = self.create_timer(1.0, self.logging_timer_callback)
        self.get_logger().info('RTF Logger pornit pe ROS 2 Jazzy. Salvare la frecvență de 1Hz...')

    def clock_callback(self, msg):
        # Doar actualizăm variabila globală din mers, operație ultra-rapidă
        self.current_sim_time = msg.clock.sec + (msg.clock.nanosec / 1e9)

    def logging_timer_callback(self):
        current_real_time = time.time()
        
        # Securitate în caz că simularea încă nu a pornit corect
        if self.current_sim_time == 0.0:
            return

        if self.last_sim_time is not None:
            delta_sim = self.current_sim_time - self.last_sim_time
            delta_real = current_real_time - self.last_real_time

            if delta_real > 0:
                rtf = delta_sim / delta_real
                
                # Limităm RTF-ul la valori logice (evităm spike-urile de inițializare)
                if rtf > 2.0: rtf = 1.0 
                
                # Scriere sigură în CSV
                self.csv_writer.writerow([round(self.current_sim_time, 2), round(current_real_time, 2), round(rtf, 4)])
                self.get_logger().info(f'Sim Time: {round(self.current_sim_time, 1)}s | RTF: {round(rtf, 2)}')

        self.last_sim_time = self.current_sim_time
        self.last_real_time = current_real_time

    def destroy_node(self):
        self.csv_file.close()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = RTFLogger()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()