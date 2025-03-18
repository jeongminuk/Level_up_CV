import cv2
import time

video_source = 0 #(웹캠)
video = cv2.VideoCapture(video_source)

# 비디오 저장 설정
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
fps = int(video.get(cv2.CAP_PROP_FPS)) if video.get(cv2.CAP_PROP_FPS) > 0 else 30  # FPS 설정
frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

output_filename = "recorded_video.mp4"
out = cv2.VideoWriter(output_filename, fourcc, fps, (frame_width, frame_height))

# 모드 설정
recording = False  # 초기 상태: 미녹화
flip_mode = False  # 초기 상태: 좌우 반전 안함

print("🎥 Video Recorder Started! Press SPACE to start/stop recording. Press ESC to exit.")

while True:
    valid, frame = video.read()
    if not valid:
        print("⚠️ 영상 프레임을 가져올 수 없습니다. 스트림을 확인하세요!")
        break
    
    if flip_mode:
        frame = cv2.flip(frame, 1) # 좌우 반전

    #녹화 중이면 저장하고, 빨간 원으로 표시
    if recording:
        out.write(frame)
        cv2.circle(frame, (50, 50), 10, (0, 0, 255), -1)  # 왼쪽 상단에 빨간 원 표시
        cv2.putText(frame, "REC", (70, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
    cv2.imshow("Video Recorder", frame)

    key = cv2.waitKey(int(1000 / fps)) & 0xFF
    if key == 32:  # SPACE 키: 녹화 시작/정지
        recording = not recording
        if recording:
            print("🔴 녹화 시작!")
        else:
            print("⏹ 녹화 중지")
    
    elif key == ord('f') or key == ord('F'):  # 'F' 키: 좌우 반전 ON/OFF
        flip_mode = not flip_mode
        print("🔄 좌우 반전 ON" if flip_mode else "🔄 좌우 반전 OFF")

    elif key == 27:  # ESC 키: 종료
        print("🛑 프로그램 종료!")
        break

video.release()
out.release()
cv2.destroyAllWindows()

print(f"✅ 녹화된 영상이 '{output_filename}' 파일로 저장되었습니다!")