# 🎮 Cute Pacman Adventure - Game Pacman với AI

## 📖 Giới thiệu

Đây là một phiên bản Pacman được thiết kế với giao diện đáng yêu và tích hợp các thuật toán AI để điều khiển ma. Game được phát triển bằng Python và thư viện Pygame, mang đến trải nghiệm chơi game vừa thú vị vừa có tính giáo dục về các thuật toán tìm đường.

## 🎯 Cơ chế hoạt động của game

### Gameplay cơ bản
- **Mục tiêu**: Điều khiển Pacman ăn hết tất cả các chấm nhỏ và viên năng lượng trên bản đồ
- **Điều khiển**: Sử dụng phím mũi tên để di chuyển Pacman
- **Điểm số**: 
  - Chấm nhỏ: +10 điểm
  - Viên năng lượng: +50 điểm
  - Ăn ma khi ở chế độ Power: +200 điểm
- **Mạng sống**: Bắt đầu với 3 mạng, mất 1 mạng khi va chạm với ma

### Chế độ Power Mode
- Khi ăn viên năng lượng (power pellet), Pacman sẽ có khả năng ăn ma trong 10 giây
- Ma sẽ chuyển sang trạng thái sợ hãi và chạy trốn
- Hiệu ứng ánh sáng đặc biệt quanh màn hình

### Hệ thống AI của ma
Mỗi con ma sử dụng một thuật toán tìm đường khác nhau:
- **Ma đỏ**: Thuật toán A* (A-star)
- **Ma hồng**: Thuật toán BFS (Breadth-First Search)
- **Ma xanh**: Thuật toán DFS (Depth-First Search)
- **Ma cam**: Di chuyển ngẫu nhiên

## 🛠️ Hướng dẫn cài đặt

### Yêu cầu hệ thống
- Python 3.7 trở lên
- Thư viện Pygame

### Các bước cài đặt

1. **Cài đặt Python**:
   - Tải và cài đặt Python từ [python.org](https://python.org)
   - Đảm bảo đã thêm Python vào PATH

2. **Cài đặt Pygame**:
   ```bash
   pip install pygame
   ```
3. **Chạy game**:
   ```
   python pacman.py
   ```
## Thuyết minh cách tạo game
### Cấu trúc dự án
Pacman/
├── pacman.py          # File chính chứa toàn bộ logic game
└── README.md          # Tài liệu hướng dẫn

### Thư viện và công cụ
import pygame          # Thư viện game engine chính
import random          # Tạo số ngẫu nhiên cho AI
import heapq           # Cấu trúc dữ liệu heap cho A*
import math            # Tính toán toán học cho animation
from collections import deque  # Queue cho BFS

### 5. Hiệu ứng Power Mode
Khi Pacman ăn viên năng lượng, bật trạng thái Power Mode trong 10 giây.
Các ma chuyển sang trạng thái sợ hãi, đổi màu và di chuyển tránh xa Pacman (có thể dùng thuật toán tìm đường ngược lại).
Hiệu ứng viền sáng hoặc nhấp nháy quanh màn hình để báo hiệu.

### 6. Xử lý âm thanh và hiệu ứng
Sử dụng pygame.mixer để phát nhạc nền, âm thanh khi ăn chấm, ăn ma, thua mạng.
Hiệu ứng chuyển cảnh, animation Pacman ăn chấm, ma đổi trạng thái.

### 7. Vòng lặp game chính
Lắng nghe sự kiện bàn phím để điều khiển Pacman.
Cập nhật vị trí Pacman và ma mỗi frame.
Kiểm tra điều kiện thắng (ăn hết chấm) hoặc thua (hết mạng).
Vẽ lại toàn bộ màn hình mỗi frame.

### 8. Tối ưu và mở rộng
Có thể mở rộng thêm nhiều màn chơi, tăng độ khó, thêm các loại ma hoặc vật phẩm đặc biệt.
Tối ưu hiệu suất bằng cách giảm số lần vẽ lại không cần thiết, sử dụng sprite sheet cho animation.