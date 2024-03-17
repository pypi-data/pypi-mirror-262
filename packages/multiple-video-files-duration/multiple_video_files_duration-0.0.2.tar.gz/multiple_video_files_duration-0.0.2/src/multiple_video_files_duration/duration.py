import os
import cv2
import datetime
import argparse


class VideoDurationCalculator:
    def __init__(self, filename):
        self.filename = filename

    def calculate_duration(self):
        video = cv2.VideoCapture(self.filename)
        fps = video.get(cv2.CAP_PROP_FPS)
        frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
        try:
            seconds = frame_count / fps
        except ZeroDivisionError:
            return datetime.timedelta(seconds=0)
        return datetime.timedelta(seconds=seconds)


class DirectoryIterator:
    def __init__(self, directory):
        self.directory = directory

    def iterate(self):
        total_duration = datetime.timedelta(seconds=0)
        for root, dirs, files in os.walk(self.directory):
            print(f"Current directory: {root}")
            print(f"Subdirectories: {dirs}")
            print(f"Files: {files}")
            for each_file in files:
                print(f"Processing File: {each_file}")
                video_file = os.path.join(root, each_file)
                video_duration_calculator = VideoDurationCalculator(video_file)
                total_duration += video_duration_calculator.calculate_duration()
            print("\n")
        return total_duration


def initialise_args():
    parser = argparse.ArgumentParser(description='Get flag values')
    parser.add_argument('-p', '--path', required=True, help='root directory for video files and sub directories')
    args = parser.parse_args()
    return args.path


def start():
    directory = initialise_args()
    directory_iterator = DirectoryIterator(directory)
    total_duration = directory_iterator.iterate()
    print(f"Total Video Duration: {total_duration}")

if __name__ == '__main__':
    start()
