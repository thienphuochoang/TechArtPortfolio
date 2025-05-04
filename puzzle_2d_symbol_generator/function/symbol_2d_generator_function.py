from serpapi import GoogleSearch
import requests, os
from general.config_loader.config_loader import ConfigLoader
from io import BytesIO
from transformers import CLIPProcessor, CLIPModel, BlipProcessor, BlipForConditionalGeneration
import torch
from PIL import Image

class Symbol2DGeneratorFunction:
    def __init__(self):
        self.settings_path = "puzzle_2d_symbol_generator/settings/settings.json"
        self.settings = ConfigLoader.load_config(self.settings_path)

        self.api_key = self.settings["api_key"]
        self.search_term = self.settings["search_term"]
        self.output_dir = os.path.join(ConfigLoader.get_root_path(), self.settings["output_dir"]).replace("\\", "/")
        self.num_images = self.settings.get("num_images", 20)  # fallback if not defined

        os.makedirs(self.output_dir, exist_ok=True)

    def search_on_google(self):
        params = {
            "engine": "google",
            "q": self.search_term,
            "tbm": "isch",  # image search
            "num": self.num_images,
            "api_key": self.api_key
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        images = results.get("images_results", [])
        images = images[:min(self.num_images, len(images))]

        for i, img in enumerate(images):
            try:
                img_url = img["original"]
                response = requests.get(img_url)
                image = Image.open(BytesIO(response.content)).convert("RGB").resize((512, 512))
                filename = f"symbol_{i + 1:03d}.jpg"
                image.save(os.path.join(self.output_dir, filename))
                print(f"Saved: {filename}")
            except Exception as e:
                print(f"Failed to download image {i}: {e}")

    def delete_irrelevant_images(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
        processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

        folder = self.output_dir
        # ✨ Give multiple options
        target_text = [
            "slot machine symbol",
            "casino icon",
            "fruit symbol from slot game",
            "slot machine sprite sheet",
            "not a slot symbol"
        ]
        threshold = self.settings.get("clip_threshold_filter", 0.85)

        for filename in os.listdir(folder):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                try:
                    image_path = os.path.join(folder, filename)
                    image = Image.open(image_path).convert("RGB")

                    inputs = processor(text=target_text, images=image, return_tensors="pt", padding=True).to(device)
                    outputs = model(**inputs)
                    probs = outputs.logits_per_image.softmax(dim=1).cpu().detach().numpy()[0]

                    best_idx = probs.argmax()
                    best_label = target_text[best_idx]
                    confidence = probs[best_idx]

                    if ("not a slot symbol" in best_label) or (confidence < threshold):
                        print(f"Removing: {filename} (Label: {best_label}, Score: {confidence:.2f})")
                        os.remove(image_path)
                    else:
                        print(f"Keeping: {filename} (Label: {best_label}, Score: {confidence:.2f})")

                except Exception as e:
                    print(f"Skipping {filename}: {e}")

    def auto_generate_captions(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"

        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)

        input_folder = self.output_dir
        output_folder = os.path.join(ConfigLoader.get_root_path(), self.settings["caption_output_dir"])
        os.makedirs(output_folder, exist_ok=True)

        for filename in os.listdir(input_folder):
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                try:
                    path = os.path.join(input_folder, filename)
                    image = Image.open(path).convert("RGB")

                    inputs = processor(images=image, return_tensors="pt").to(device)
                    out = model.generate(**inputs)
                    caption = processor.decode(out[0], skip_special_tokens=True)

                    # Filter out non-slot content (optional): simple heuristic
                    if "symbol" not in caption.lower() and "slot" not in caption.lower():
                        print(f"Removed: {filename} — Caption: '{caption}'")
                        os.remove(path)
                        continue

                    new_filename = os.path.join(output_folder, filename)
                    image.save(new_filename)
                    with open(new_filename.replace(".png", ".txt").replace(".jpg", ".txt"), "w") as f:
                        f.write(caption)

                    print(f"Kept: {filename} — Caption: '{caption}'")

                except Exception as e:
                    print(f"Error processing {filename}: {e}")