# Otonom Araba Projesi (ROS2 + Gazebo)

RPi5 + kamera tabanlı, YOLO ile hedef tespiti yapan otonom bir arabanın 
ROS2/Gazebo simülasyon ortamında geliştirilmesi.

## Ortam
- Ubuntu 24.04 LTS
- ROS2 Jazzy Jalisco
- Gazebo Harmonic (ros-jazzy-ros-gz)
- slam_toolbox

## Yapı
- `worlds/` — Gazebo dünya/SDF dosyaları
                                 
## Durum
- FSM tabanlı hareket kontrolcüsü (HEDEF_SEC / DON / ILERLE) çalışıyor
- Lidar tabanlı reaktif engelden kaçınma entegre edildi
- SLAM (slam_toolbox) TurtleBot3 ile test edildi
