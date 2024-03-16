from direct.showbase.ShowBase import ShowBase
import os
from PIL import Image, ImageSequence, ImageDraw, ImageFont
import requests
from io import BytesIO
import sys
import subprocess
import os
from panda3d.core import PNMImage
from panda3d.core import Filename
from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3, loadPrcFileData, FrameBufferProperties, WindowProperties, GraphicsPipe
import fcntl
import hashlib
import time

class ModelViewer(ShowBase):
    def __init__(self, model_path, image_path, save_path, frames, filename, top_text, bottom_text, speed, bg_color,
                 model_pos=(0, 0, 0), model_hpr=(0, 96, 25), 
                 cam_pos=(0, -3, 0)):

        #getModelPath().appendDirectory("/Users/overtime/Documents/GitHub/NyanStreamer/assets/models")
        loadPrcFileData("", "window-type offscreen")
        loadPrcFileData("", "audio-library-name null")
        ShowBase.__init__(self)

        self.model_path = model_path
        self.frames = []
        self.frame_counter = 0
        self.total_frames = frames  # Adjust this value for the number of frames you want
        self.rotation_speed = 360.0 / self.total_frames  # Automatically adjust rotation speed based on total frames
        self.filename = filename
        self.top_text = top_text
        self.bottom_text = bottom_text
        self.speed = speed
        self.bg_color = bg_color

        # Check if the model is in .obj format
        if self.model_path.endswith('.obj'):
            print("Converting .obj to .egg...")
            egg_path = self.model_path.replace('.obj', '.egg')
            subprocess.run(['obj2egg', '-o', egg_path, self.model_path])
            if not os.path.exists(egg_path):
                print("Failed to convert .obj to .egg.")
                return
            self.model_path = egg_path
            print(".obj converted to .egg successfully!")
            
        # Load the 3D model
        print("Loading the 3D model...")
        self.model = self.loader.loadModel(self.model_path)
        if not self.model:
            print("Failed to load the model.")
            return
        print("Model loaded successfully!")

        # Scale the model to fit the view
        min_point, max_point = self.model.getTightBounds()
        max_dim = max_point - min_point
        scale_factor = 1.8 / max_dim.length()
        self.model.setScale(scale_factor)  # Zoom in by scaling the model up


        # Load and apply the texture
        if image_path.startswith('http'):
            # Download the texture
            response = requests.get(image_path)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
        else:
            # Open the image file directly
            image = Image.open(image_path)

        # If the image is a GIF, get its first frame
        if image.is_animated:
            image = ImageSequence.Iterator(image)[0]

        # Handle transparency by filling with specified background color
        if image.mode == 'RGBA':
            background = Image.new('RGB', image.size, self.hex_to_rgb(self.bg_color))
            background.paste(image, mask=image.split()[3])  # 3 is the alpha channel
            image = background

        # Resize the image to 16:9
        image = image.resize((1920, 1080))

        # Save as PNG
        image.save(save_path, "PNG")

        self.texture = self.loader.loadTexture(save_path)
        self.model.setTexture(self.texture, 1)

        # Position the model
        self.model.setPos(*model_pos)
        self.model.setHpr(*model_hpr)
        self.model.reparentTo(self.render)

        # Set up the camera
        self.cam.setPos(*cam_pos)  # Move the camera closer
        #self.cam.lookAt(self.model)

        # Set up lighting
        self.setup_lighting()

        # Set up offscreen buffer for capturing frames
        self.setup_offscreen_buffer()

        # Start the spinning task
        self.taskMgr.add(self.spin_task, "spin_task")
        #after the task is done, close the window

    def setup_lighting(self):
        from panda3d.core import AmbientLight, DirectionalLight

        # Ambient light
        ambient = AmbientLight("ambient_light")
        ambient.setColor((0.2, 0.2, 0.2, 1))
        ambient_np = self.render.attachNewNode(ambient)
        self.render.setLight(ambient_np)

        # Directional light
        directional = DirectionalLight("directional_light")
        directional.setDirection(Vec3(0, 8, -2.5))
        directional.setColor((1, 1, 1, 1))
        directional_np = self.render.attachNewNode(directional)
        self.render.setLight(directional_np)

    def setup_offscreen_buffer(self):
        # Create offscreen buffer
        fb_props = FrameBufferProperties()
        fb_props.setRgbaBits(8, 8, 8, 8)
        fb_props.setDepthBits(1)
        win_props = WindowProperties.size(self.win.getXSize(), self.win.getYSize())
        self.buffer = self.graphicsEngine.makeOutput(self.pipe, "offscreen buffer", -2, fb_props, win_props,
                                                     GraphicsPipe.BFRefuseWindow, self.win.getGsg(), self.win)
        self.buffer.setClearColor(self.hex_to_rgb(self.bg_color) + (1,))

        # Set up the display region
        dr = self.buffer.makeDisplayRegion()
        dr.setCamera(self.cam)
        
    def remove_background(self, input_path, output_path):
        """Remove background using ImageMagick."""
        cmd = [
            'convert', input_path, 
            '-fuzz', '10%',  # Adjust this value if needed
            '-fill', 'none',
            '-opaque', self.bg_color,
            output_path
        ]
        subprocess.run(cmd)

    def add_text_to_frame(self, frame_path):
        frame = Image.open(frame_path)
        draw = ImageDraw.Draw(frame)
        font = ImageFont.truetype("arial.ttf", 36)

        if self.top_text != "":
            text_width, text_height = draw.textsize(self.top_text, font)
            x = (frame.width - text_width) // 2
            y = 20
            draw.text((x, y), self.top_text, font=font, fill=(255, 255, 255))

        if self.bottom_text != "":
            text_width, text_height = draw.textsize(self.bottom_text, font)
            x = (frame.width - text_width) // 2
            y = frame.height - text_height - 20
            draw.text((x, y), self.bottom_text, font=font, fill=(255, 255, 255))

        frame.save(frame_path)

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def spin_task(self, task):
        self.model.setH(self.model.getH() + self.rotation_speed)
        if self.frame_counter < self.total_frames:
            frame_path = os.path.join("assets/frames", f"frame_{self.frame_counter}.png")
            img = PNMImage()
            self.buffer.getScreenshot(img)
            img.write(frame_path)

            # Remove background from the captured frame
            no_bg_path = os.path.join("assets/frames", f"frame_no_bg_{self.frame_counter}.png")
            self.remove_background(frame_path, no_bg_path)

            # Add text to the frame
            self.add_text_to_frame(no_bg_path)

            self.frames.append(no_bg_path)
            self.frame_counter += 1
            print(f"Frame {self.frame_counter} captured.")
            return task.cont
        else:
            frames = [Image.open(frame_path) for frame_path in self.frames]
            reference_frame_count = 36
            reference_duration_per_frame = 50  # 50 milliseconds for 36 frames
            actual_frame_count = len(frames)
            desired_duration_per_frame = (reference_frame_count * reference_duration_per_frame) // actual_frame_count
            desired_duration_per_frame = int(desired_duration_per_frame * self.speed)  # Adjust duration based on speed
            with open(f'{self.filename}.gif', 'wb') as f:
                fcntl.flock(f, fcntl.LOCK_EX)  # Acquire an exclusive lock
                frames[1].save(f, save_all=True, append_images=frames[2:], duration=desired_duration_per_frame, loop=0, disposal=2)
                fcntl.flock(f, fcntl.LOCK_UN)  # Release the lock
            print(f"GIF created: {self.filename}.gif")

def spinning_model(model_path: str, image_path: str, frames: int, filename: str, top_text: str, bottom_text: str, speed: float, bg_color: str,
                   model_pos: tuple = (0, 0, 0), 
                   model_hpr: tuple = (0, 0, 0), 
                   cam_pos: tuple = (0, -3, 0)):
    
    # Generate a hash of the image_path
    hash_object = hashlib.md5(image_path.encode())
    hex_dig = hash_object.hexdigest()

    # Combine the hash with the current timestamp to generate a unique filename
    timestamp = int(time.time())
    save_path = f"download_{hex_dig}_{timestamp}.png"
    app = ModelViewer(model_path, image_path, save_path, frames, filename, top_text, bottom_text, speed, bg_color, model_pos, model_hpr, cam_pos)
    app.run()
    
    if os.path.exists(save_path):
        os.remove(save_path)