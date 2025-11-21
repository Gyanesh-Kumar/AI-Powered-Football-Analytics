from utils import read_video, save_video
import cv2
from trackers import Tracker
from player_ball_assigner import PlayerBallAssigner
import numpy as np
from team_assigner import TeamAssigner
from camera_movement_estimator import CameraMovementEstimator
from view_transformer import ViewTransformer
from speed_and_distance_estimator import SpeedAndDistance_Estimator
import json

def main():
    video_frames = read_video('input_videos/A1606b0e6_0 (19).mp4')

    tracker = Tracker('models/best.pt')

    tracks = tracker.get_object_tracks(video_frames)

    tracker.add_position_to_tracks(tracks)

    # Assuming you've completed tracking and have `tracks` dictionary
    target_track_id = 11  # Replace with the ID you want to trace
    track_path = tracker.extract_track_path(tracks, target_track_id)
    # Plot the movement path for the chosen track ID
    tracker.plot_player_movement(track_path, target_track_id)
    
    player_bbox = tracker.get_bounding_box(tracks, target_track_id)
    # Specify the path and name of the JSON file you want to save to
    output_file = 'player_bounding_box_2.json'

    # Save to JSON
    with open(output_file, 'w') as file:
        json.dump(player_bbox, file, indent=4)  # indent=4 for pretty-printing

    pb = tracker.get_logs(video_frames, tracks)
    output_file_1 = 'pb.json'
    with open(output_file_1, 'w') as file:
        json.dump(pb, file, indent=4)  # indent=4 for pretty-printing

    camera_movement_estimator = CameraMovementEstimator(video_frames[0])
    camera_movement_per_frame = camera_movement_estimator.get_camera_movement(video_frames)
    camera_movement_estimator.add_adjust_positions_to_tracks(tracks,camera_movement_per_frame)

    view_transformer = ViewTransformer()
    view_transformer.add_transformed_position_to_tracks(tracks)

    tracks["ball"] = tracker.interpolate_ball_positions(tracks["ball"])
    # tracker.plot_ball_movement(track_path, tracks["ball"])

    speed_and_distance_estimator = SpeedAndDistance_Estimator()
    speed_and_distance_estimator.add_speed_and_distance_to_tracks(tracks)

    team_assigner = TeamAssigner()
    team_assigner.assign_team_color(video_frames[0], 
                                    tracks['players'][0])
    
    for frame_num, player_track in enumerate(tracks['players']):
        for player_id, track in player_track.items():
            team = team_assigner.get_player_team(video_frames[frame_num],   
                                                 track['bbox'],
                                                 player_id)
            tracks['players'][frame_num][player_id]['team'] = team 
            tracks['players'][frame_num][player_id]['team_color'] = team_assigner.team_colors[team]


    # save cropped image of a player
    for track_id, player in tracks['players'][0].items():
        bbox = player['bbox']
        frame = video_frames[0]

        # crop bbox from frame
        cropped_image = frame[int(bbox[1]):int(bbox[3]),int(bbox[0]):int(bbox[2])]

        # save the cropped image
        cv2.imwrite(f'output_videos/cropped_image3.jpg',cropped_image)
        break


    # Debugging version of code to capture and verify a single player's image
    # for track_id, player in tracks['players'][0].items():
    #     bbox = player['bbox']
    #     frame = video_frames[0]

    #     # Print the bounding box to verify its coordinates
    #     print(f"Track ID: {track_id}, Bounding Box: {bbox}")

    #     # Ensure bbox coordinates are integers and valid for slicing
    #     x1, y1, x2, y2 = map(int, [bbox[0], bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3]])

    #     # Check if the coordinates are within frame dimensions
    #     if (0 <= x1 < frame.shape[1] and 0 <= x2 <= frame.shape[1] and 
    #         0 <= y1 < frame.shape[0] and 0 <= y2 <= frame.shape[0]):
        
    #         # Crop the image based on the bounding box
    #         cropped_image = frame[y1:y2, x1:x2]
        
    #         # Save the cropped image
    #         cv2.imwrite(f'output_videos/cropped_player_{track_id}.jpg', cropped_image)
    #         print(f"Saved cropped image for player {track_id}.")

    #         # Break after saving the first player's image
    #         break
    #     else:
    #         print(f"Bounding box for player {track_id} is out of frame bounds.")



    player_assigner =PlayerBallAssigner()
    team_ball_control= []
    for frame_num, player_track in enumerate(tracks['players']):
        ball_bbox = tracks['ball'][frame_num][1]['bbox']
        assigned_player = player_assigner.assign_ball_to_player(player_track, ball_bbox)

        if assigned_player != -1:
            tracks['players'][frame_num][assigned_player]['has_ball'] = True
            team_ball_control.append(tracks['players'][frame_num][assigned_player]['team'])
        else:
            team_ball_control.append(team_ball_control[-1])
    team_ball_control= np.array(team_ball_control)
                                       
    
    output_video_frames = tracker.draw_annotations(video_frames, tracks, team_ball_control)

    output_video_frames = camera_movement_estimator.draw_camera_movement(output_video_frames,camera_movement_per_frame)

    speed_and_distance_estimator.draw_speed_and_distance(output_video_frames,tracks)

    save_video(output_video_frames, 'output_videos/output_video2.avi')



if __name__ == '__main__':
    main()