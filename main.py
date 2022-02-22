import os
import numpy as np

from PIL import Image
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup


class LoadDialog(FloatLayout):
    """
    LoadDialog widget class
    """
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    current_path = os.path.dirname(__file__)

    def get_path(self):
        """
        Returns current folder path
        :return: current path
        """
        return self.current_path


class ThresholdDialog(FloatLayout):
    """
    ThresholdDialog widget class
    """
    process = ObjectProperty(None)
    cancel = ObjectProperty(None)


class Root(FloatLayout):
    """
    Root widget class
    """
    image_file = ObjectProperty(None)
    grayscale_button = ObjectProperty(None)
    binarize_button = ObjectProperty(None)
    current_image = 'default.png'

    def dismiss_popup(self):
        """
        Closes popup window
        """
        self._popup.dismiss()

    def show_load(self):
        """
        Displays load dialog window
        :return: files and folders list
        """
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        """
        Sets image file name
        :param path: file path
        :param filename: image file name
        :return: source file name and path info
        """
        try:
            if os.path.exists('grayscale.png'):
                os.remove('grayscale.png')
            if os.path.exists('binarized.png'):
                os.remove('binarized.png')
            LoadDialog.current_path = path
            self.current_image = filename[0]
            self.image_file.source = os.path.join(LoadDialog.current_path, self.current_image)
            self.grayscale_button.disabled = False
            self.binarize_button.disabled = True
        except:
            pass

        self.dismiss_popup()

    def convert_grayscale(self):
        """
        Converts an image to grayscale
        :return: None
        """
        try:
            img = Image.open(os.path.join(LoadDialog.current_path, self.current_image)).convert('L')
            img.save('grayscale.png')
            self.image_file.source = 'grayscale.png'
            self.image_file.reload()
            self.binarize_button.disabled = False
        except:
            pass

        self.grayscale_button.disabled = True

    def binarization(self, th_l, th_h):
        """
        Image binarization
        :return: None
        """
        try:
            mean_val = int((th_h + th_l) / 2)
            img = np.array(Image.open('grayscale.png'))
            img_bin_l = (img > th_l) * mean_val
            img_bin_h = (img > th_h) * (255 - mean_val)
            img_final = img_bin_h + img_bin_l

            Image.fromarray(np.uint8(img_final)).save('binarized.png')
            self.image_file.source = 'binarized.png'
            self.image_file.reload()
        except:
            pass

        self.dismiss_popup()

    def show_threshold(self):
        """
        Displays threshold setting dialog window
        :return: the two threshold: low and high
        """
        content = ThresholdDialog(process=self.binarization, cancel=self.dismiss_popup)
        self._popup = Popup(title="Threshold settings", content=content,
                            size_hint=(0.95, None), height=90)
        self._popup.open()


class PictureViewerApp(App):
    pass


Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('ThresholdDialog', cls=ThresholdDialog)

if __name__ == '__main__':
    PictureViewerApp().run()
