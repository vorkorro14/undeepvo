import os

import pykitti
from google_drive_downloader import GoogleDriveDownloader as gdd


class Downloader(object):
    def __init__(self, sequence_id='08', main_dir='dataset'):
        self.sequence_id = sequence_id
        self.main_dir = main_dir
        self.sequence = Sequence(self.sequence_id, self.main_dir)
        if not os.path.exists(self.main_dir):
            os.mkdir(self.main_dir)

    def download_sequence(self):
        gdd.download_file_from_google_drive(file_id=self.sequence.calib.id, dest_path=self.sequence.calib.name,
                                            unzip=True)
        os.rename(os.path.join(os.curdir, self.main_dir, 'sequences', self.sequence_id, 'calib.txt'),
                  os.path.join(os.curdir, self.main_dir, 'sequences', self.sequence_id, 'calib1.txt'))
        gdd.download_file_from_google_drive(file_id=self.sequence.poses.id, dest_path=self.sequence.poses.name,
                                            unzip=True)
        gdd.download_file_from_google_drive(file_id=self.sequence.images.id, dest_path=self.sequence.images.name,
                                            unzip=True)
        os.remove(os.path.join(os.curdir, self.main_dir, 'sequences', self.sequence_id, 'calib.txt'))
        os.rename(os.path.join(os.curdir, self.main_dir, 'sequences', self.sequence_id, 'calib1.txt'),
                  os.path.join(os.curdir, self.main_dir, 'sequences', self.sequence_id, 'calib.txt'))
        self.clean_space()
        self.pykiti_sequence()

    def clean_space(self):
        os.remove(self.sequence.calib.name)
        os.remove(self.sequence.poses.name)
        os.remove(self.sequence.images.name)

    def pykiti_sequence(self, frames=range(0, 20, 5)):
        self.dataset = pykitti.odometry(self.sequence.main_dir, self.sequence.sequence_id, frames=frames)


class Sequence(object):
    def __init__(self, sequence_id='08', main_dir='dataset'):
        self.sequence_id = sequence_id
        self.main_dir = main_dir
        self.calib = Kitti_link('data_odometry_calib.zip', '1jW1Yr8qBD2m63QQjN_q_EJWiQIyhtFj0')
        self.poses = Kitti_link('data_odometry_poses.zip', '1m1J7T_1hvrIWbT14m9KDSrffgqhUaEfL')
        self.images = Kitti_link('data_odometry_color.zip', '1s6GhV8UQHdZjWaX1pcJy_8TZ9rbT-21C', ins=True,
                                 main_dir=self.main_dir)


class Kitti_link(object):
    def __init__(self, name, id, ins=False, main_dir='dataset'):
        if ins:
            self.name = os.path.join(os.curdir, main_dir, 'sequences', name)
        else:
            self.name = os.path.join(os.curdir, name)
        self.id = id


if __name__ == '__main__':
    s8 = Downloader('08')
    s8.download_sequence()
    s8.pykiti_sequence(range(0, 100, 10))
