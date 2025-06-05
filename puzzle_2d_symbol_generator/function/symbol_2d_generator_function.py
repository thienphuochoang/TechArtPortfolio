from serpapi import GoogleSearch
import requests, os
from general.config_loader.config_loader import ConfigLoader
from io import BytesIO
from transformers import CLIPProcessor, CLIPModel, BlipProcessor, BlipForConditionalGeneration
import torch
from PIL import Image
from typing import List
from leonardo_ai_sdk import LeonardoAiSDK
from leonardo_ai_sdk.models.shared.job_status import JobStatus
import asyncio
import time
from general.image_manager.image_manager import ImageManager
from segment_anything import SamAutomaticMaskGenerator, sam_model_registry
import cv2

class Symbol2DGeneratorFunction:
    def __init__(self):
        self.settings_path = "puzzle_2d_symbol_generator/settings/settings.json"
        self.settings = ConfigLoader.load_config(self.settings_path)
        self.root_path = ConfigLoader.get_root_path()

        self.api_key = self.settings["external_settings"]["google_api_key"]
        self.search_term = self.settings["external_settings"]["search_term"]
        self.output_dir = os.path.join(self.root_path, self.settings["external_settings"]["output_dir"]).replace("\\", "/")
        self.num_images = self.settings.get("num_images", 20)  # fallback if not defined

        os.makedirs(self.output_dir, exist_ok=True)

        self.models_data = [
            {"name": "Kino 2.0", "id": "05ce0082-2d80-4a2d-8653-4d1c85e2418e",
             "url": "https://cdn.leonardo.ai/users/8eab0214-1c27-4124-b152-84d3236fe7a4/generations/6ff249be-6b8d-49ae-a8e6-496b63b544ff/b51b5b4a-5b71-485b-a3fc-91c00e68aedf.jpg"},
            {"name": "Leonardo Phoenix 1.0", "id": "de7d3faf-762f-48e0-b3b7-9d0ac3a3fcf3",
             "url": "https://cdn.leonardo.ai/users/d35cac34-28ff-4c33-8022-ebc672a45aca/generations/a0bfc1a1-f623-4646-a090-1e41fe4c2f37/segments/2:2:2/Leonardo_Phoenix_Image_is_a_digital_artwork_featuring_a_vibran_0.jpg"},
            {"name": "Flux Dev", "id": "b2614463-296c-462a-9586-aafdb8f00e36",
             "url": "https://cdn.leonardo.ai/users/384ab5c8-55d8-47a1-be22-6a274913c324/generations/e20fbbc2-1810-411c-8937-7504c994ef4c/thumbnail.jpg"},
            {"name": "Flux Schnell", "id": "1dd50843-d653-4516-a8e3-f0238ee453ff",
             "url": "https://cdn.leonardo.ai/users/384ab5c8-55d8-47a1-be22-6a274913c324/generations/063d615b-7fba-41e3-bda7-e3413e55731d/thumbnail.jpg"},
            {"name": "Leonardo Phoenix 0.9", "id": "6b645e3a-d64f-4341-a6d8-7a3690fbf042",
             "url": "https://cdn.leonardo.ai/users/384ab5c8-55d8-47a1-be22-6a274913c324/generations/5e150d17-c580-4ec4-afb6-719884213508/Default_A_majestic_phoenix_wrapped_around_stylized_title_text_0.jpg"},
            {"name": "Leonardo Anime XL", "id": "e71a1c2f-4f80-4800-934f-2c68979d8cc8",
             "url": "https://cdn.leonardo.ai/users/384ab5c8-55d8-47a1-be22-6a274913c324/generations/16cbffcc-8672-47d6-8738-d22167dcea3f/Default_A_lush_vibrant_anime_hero_figure_emerges_from_the_shad_0.jpg"},
            {"name": "Leonardo Lightning XL", "id": "b24e16ff-06e3-43eb-8d33-4416c2d75876",
             "url": "https://cdn.leonardo.ai/users/384ab5c8-55d8-47a1-be22-6a274913c324/generations/334022a8-7cea-43f9-a8a0-b9c2d232f32f/Default_an_ageing_astronaut_piloting_an_old_spaceship_0.jpg"},
            {"name": "SDXL 1.0", "id": "16e7060a-803e-4df3-97ee-edcfa5dc9cc8",
             "url": "https://cdn.leonardo.ai/users/8d579b04-03c4-4d41-8132-99e6cc6864b2/generations/834b80d5-b42e-4200-b5be-1929710106db/Default_A_stunningly_crafted_oneofakind_electric_guitar_adorne_0.jpg"},
            {"name": "Leonardo Kino XL", "id": "aa77f04e-3eec-4034-9c07-d0f619684628",
             "url": "https://cdn.leonardo.ai/users/384ab5c8-55d8-47a1-be22-6a274913c324/generations/38c684e6-702f-446a-b99b-649462d6a3d6/Leonardo_Kino_XL_cinematic_photo_of_a_surreal_adventurer_on_a_2.jpg"},
            {"name": "Leonardo Vision XL", "id": "5c232a9e-9061-4777-980a-ddc8e65647c6",
             "url": "https://cdn.leonardo.ai/users/384ab5c8-55d8-47a1-be22-6a274913c324/generations/bc0a7117-ad5e-4754-8648-6412cc554478/Leonardo_Vision_XL_A_gritty_unedited_photograph_perfectly_capt_2.jpg"},
            {"name": "DreamShaper v7", "id": "ac614f96-1082-45bf-be9d-757f2d31c174",
             "url": "https://cdn.leonardo.ai/users/384ab5c8-55d8-47a1-be22-6a274913c324/generations/bff69fae-6e4e-48d1-8a8f-6c75799be511/DreamShaper_v7_an_older_tired_and_battleworn_male_detective_hi_1.jpg"},
            {"name": "Absolute Reality v1.6", "id": "e316348f-7773-490e-adcd-46757c738eb7",
             "url": "https://cdn.leonardo.ai/users/384ab5c8-55d8-47a1-be22-6a274913c324/generations/9d7e2dbe-6dff-4bf5-b487-414dee2a10b9/Absolute_Reality_v16_a_stunning_photo_of_a_woman_with_aztech_t_1.jpg"},
            {"name": "Anime Pastel Dream", "id": "1aa0f478-51be-4efd-94e8-76bfc8f533af",
             "url": "https://cdn.leonardo.ai/users/384ab5c8-55d8-47a1-be22-6a274913c324/generations/8cc624c3-c1ba-40c9-b3cd-21056382728a/AnimePastelDream_fuji_film_candid_portrait_o_a_black_woman_wea_2.jpg"},
            {"name": "DreamShaper v6", "id": "b7aa9939-abed-4d4e-96c4-140b8c65dd92",
             "url": "https://cdn.leonardo.ai/users/384ab5c8-55d8-47a1-be22-6a274913c324/generations/8ab5c76a-eefb-4801-817f-458f68958db7/DreamShaperV6_a_masterpiece_image_of_Splash_art_music_album_ar_6.jpg"},
            {"name": "DreamShaper v5", "id": "d2fb9cf9-7999-4ae5-8bfe-f0df2d32abf8",
             "url": "https://cdn.leonardo.ai/users/384ab5c8-55d8-47a1-be22-6a274913c324/generations/bb22942b-40c8-4a06-a219-238808053ee0/DreamShaper_v5_extremely_intricate_fantasy_character_photoreal_0.jpg"},
            {"name": "Leonardo Diffusion", "id": "b820ea11-02bf-4652-97ae-9ac0cc00593d",
             "url": "https://cdn.leonardo.ai/users/384ab5c8-55d8-47a1-be22-6a274913c324/generations/8905a8f0-9219-43ad-8ecb-1c37b4501dc5/Leonardo_Diffusion_ultra_detailed_artistic_photography_of_a_fashion_moden_3.jpg"},
            {"name": "RPG 4.0", "id": "a097c2df-8f0c-4029-ae0f-8fd349055e61",
             "url": "https://cdn.leonardo.ai/users/b35decec-845a-475a-960f-a690332c3cf3/generations/926c827d-3504-4541-b4ff-49c5f4487858/RPG_Photography_of_a_well_built_modern_cottage_house_sitting_on_t_0.jpg"},
            {"name": "Deliberate 1.1", "id": "458ecfff-f76c-402c-8b85-f09f6fb198de",
             "url": "https://cdn.leonardo.ai/users/2e1f21ed-7ca4-4f78-80ed-1646ea463a01/generations/ddf7239c-4972-429b-8a0a-1de6f9647738/Deliberate_High_detail_RAW_color_art_animation_cartoon_magical_atmospher_0.jpg"},
            {"name": "Vintage Style Photography", "id": "17e4edbf-690b-425d-a466-53c816f0de8a",
             "url": "https://cdn.leonardo.ai/users/4e397cdd-4af3-48e5-b0e7-c2b5d1ebee59/generations/7a6f17f3-689c-461d-9c59-14a7ac88fa0e/Vintage_Style_Photography_Classic_convertible_driving_on_an_open_road_vintage_style_2.jpg"},
            {"name": "DreamShaper 3.2", "id": "f3296a34-9aef-4370-ad18-88daf26862c3",
             "url": "https://cdn.leonardo.ai/users/384ab5c8-55d8-47a1-be22-6a274913c324/generations/b2919072-7c52-409e-9c2a-11d56c5c2ed2/DreamShaper_32_Full_body_Beautiful_final_fantasy_style_portrait_clean_detai_2.jpg"}
        ]

    def get_dataset_folders(self) -> List[str]:
        dataset_dir = os.path.join(self.root_path, "puzzle_2d_symbol_generator", "dataset")
        if not os.path.exists(dataset_dir):
            print("Dataset folder not found:", dataset_dir)
            return []

        folder_names = [f for f in os.listdir(dataset_dir) if os.path.isdir(os.path.join(dataset_dir, f))]
        return folder_names

    def get_current_dataset_folder(self, current_folder) -> str:
        dataset_dir = os.path.join(self.root_path, "puzzle_2d_symbol_generator", "dataset")
        if not os.path.exists(dataset_dir):
            print("Dataset folder not found:", dataset_dir)
            return ""

        return os.path.join(dataset_dir, current_folder)

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

    def auto_generate_captions(self, output_dir):
        device = "cuda" if torch.cuda.is_available() else "cpu"

        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)

        # output_folder = self.get_current_dataset_folder(output_dir)
        output_folder = os.path.join(self.root_path, self.settings["slice_output_dir"])
        input_folder = output_folder
        os.makedirs(output_folder, exist_ok=True)

        for filename in os.listdir(input_folder):
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                try:
                    path = os.path.join(input_folder, filename)
                    image = Image.open(path).convert("RGB")

                    inputs = processor(images=image, return_tensors="pt").to(device)
                    out = model.generate(**inputs)
                    caption = processor.decode(out[0], skip_special_tokens=True)

                    new_filename = os.path.join(output_folder, filename)
                    image.save(new_filename)
                    with open(new_filename.replace(".png", ".tag").replace(".jpg", ".tag"), "w") as f:
                        f.write(caption)

                    print(f"Kept: {filename} — Caption: '{caption}'")

                except Exception as e:
                    print(f"Error processing {filename}: {e}")

    def slice_with_sam(self, min_area=400):
        # Load SAM model once
        model_type = "vit_h"
        checkpoint_path = os.path.join(self.root_path, self.settings["segment_anything_settings"]["checkpoint_path"])
        output_dir = os.path.join(self.root_path, self.settings["slice_output_dir"])
        device = "cuda" if torch.cuda.is_available() else "cpu"
        sam = sam_model_registry[model_type](checkpoint=checkpoint_path).to(device)
        mask_generator = SamAutomaticMaskGenerator(sam)

        leonardo_ai_output_dir = self.settings["leonardo_ai_settings"]["output_dir"]
        input_dir = os.path.join(self.root_path, leonardo_ai_output_dir).replace("\\", "/")
        os.makedirs(output_dir, exist_ok=True)

        for filename in os.listdir(input_dir):
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                try:
                    image_path = os.path.join(input_dir, filename)
                    image = cv2.imread(image_path)

                    if image is None:
                        print(f"Skipping unreadable file: {filename}")
                        continue

                    masks = mask_generator.generate(image)

                    count = 0
                    for idx, mask in enumerate(masks):
                        x, y, w, h = mask["bbox"]
                        if w * h < min_area:
                            continue  # Skip tiny segments

                        crop = image[y:y + h, x:x + w]
                        slice_filename = f"{os.path.splitext(filename)[0]}_slice_{count:03d}.png"
                        cv2.imwrite(os.path.join(output_dir, slice_filename), crop)
                        count += 1

                    print(f"Sliced {filename} into {count} segments with SAM.")

                except Exception as e:
                    print(f"Error slicing {filename} with SAM: {e}")

    async def generate_image(self):
        API_KEY = "ff554eca-af80-4ace-a9ec-ce1f3610729c"
        MODEL_ID = "2067ae52-33fd-4a82-bb92-c2c55e7d2786"

        request_payload = {
            "prompt": "Sprite sheet of classic fruit slot machine symbols, including cherries, lemons, grapes, oranges, watermelons, and plums. Each fruit is colorful, centered inside its own frame, vibrant cartoon style, high gloss, isolated on a white background, symmetrical layout, evenly spaced, simple background, 2D game asset, professional quality",
            "modelId": MODEL_ID,
            "width": 512,
            "height": 512,
            "num_images": 2,
            "promptMagic": False  # Set to True if your plan includes Prompt Magic
        }

        leonardo_ai_output_dir = self.settings["leonardo_ai_settings"]["output_dir"]
        output_dir = os.path.join(self.root_path, leonardo_ai_output_dir).replace("\\","/")

        with LeonardoAiSDK(bearer_auth=API_KEY) as las_client:
            res = await asyncio.to_thread(las_client.image.create_generation, request=request_payload)
            generation_id = res.object.sd_generation_job.generation_id
            print(f"Generation submitted: {generation_id}")

            # Wait for generation to complete (max 2 minutes)
            start_time = time.time()
            timeout = 120  # seconds

            while time.time() - start_time < timeout:
                result = await asyncio.to_thread(las_client.image.get_generation_by_id, id=generation_id)
                generation = result.object.generations_by_pk

                if generation.status == JobStatus.COMPLETE:
                    print("Images are ready:")
                    if generation.generated_images:
                        for idx, img in enumerate(generation.generated_images):
                            image_name = f"image_{idx + 1:03d}.jpg"
                            ImageManager.save_image_from_url(output_dir, image_name, img.url)
                            print("Image URL:", img.url)
                        return
                    else:
                        print("Generation completed but no images found.")
                        return
                elif generation.status == JobStatus.FAILED:
                    print("Generation failed.")
                    return
                else:
                    print(f"Waiting... Status: {generation.status}")
                    await asyncio.sleep(5)

            print("Timed out waiting for generation.")

