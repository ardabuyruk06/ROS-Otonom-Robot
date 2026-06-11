# Otonom Kütüphane Robotu ve QR Kod Doğrulama Sistemi

## Proje Bilgileri
* Proje Adı: ROS Noetic Kütüphane Devriye Robotu
* Geliştirici: Arda Buyruk
* Platform: ROS Noetic / Ubuntu 20.04 (Docker)
* Robot Modeli: TurtleBot3 Waffle Pi

## Proje Özeti
Bu proje, Gazebo simülasyon ortamındaki bir kütüphanede otonom olarak devriye atan bir mobil robotun yazılımını içerir. Robot sırasıyla 4 farklı istasyona (Danışma, Bilim, Roman ve Kasa bölümleri) gider, engellerden kaçarak hedefe ulaşır ve her istasyonda bulunan QR kodları kamerasıyla okuyarak doğrulama yapar.

**Proje Çalışma Videosu:** [Google Drive Üzerinden İzlemek İçin Tıklayın](https://drive.google.com/file/d/1i9u8ddnOXVe6wuMGBMIA6ZcsN-twdzj9/view?usp=sharing)

## Çalışma Mantığı
Sistem birbirine entegre 3 ana düğüm (node) ile çalışır:
1. QR Yerleştirici (spawn_qrs.py): Simülasyon başladığında QR kod panellerini haritadaki ilgili koordinatlara yerleştirir.
2. Kamera Okuyucu (qr_reader_node.py): Robotun RGB kamerasını kullanarak etraftaki QR kodları tarar ve veriyi anlık olarak yayınlar.
3. Görev Yöneticisi (task_manager_node.py): Robotun hedeflere gitmesini sağlayan otonom navigasyon (move_base) sürecini ve QR doğrulama işlemlerini yönetir.

## Çalıştırma Adımları
Sistemi tam otonom başlatmak için 4 ayrı terminalde sırasıyla şu işlemler yapılmalıdır:

Terminal 1 (Gazebo Simülasyonu):
export TURTLEBOT3_MODEL=waffle_pi
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:/root/finalodev/src/finalodev/models
roslaunch finalodev simulasyon.launch

Terminal 2 (Navigasyon ve Rviz):
export TURTLEBOT3_MODEL=waffle_pi
roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=/root/finalodev/src/finalodev/maps/map.yaml

Terminal 3 (QR Kurulum ve Okuma):
python3 /root/finalodev/src/finalodev/scripts/spawn_qrs.py
rosrun finalodev qr_reader_node.py _duplicate_timeout:=0.0

Terminal 4 (Görev Başlatma):
rosrun finalodev task_manager_node.py
