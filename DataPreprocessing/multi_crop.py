import os
import cv2
import argparse

def multi_crop(input_folder, output_folder, width, height):
    """
    For each image in 'input_folder', lets the user select multiple regions (ROIs).
    Each ROI is cropped and resized to (width, height) and saved to 'output_folder'.

    Args:
        input_folder (str): Path to the folder containing input images.
        output_folder (str): Path to the folder where cropped images will be saved.
        width (int): The desired width to resize each crop.
        height (int): The desired height to resize each crop.
    """

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Collect all image files from the input folder
    valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff')
    file_list = [
        f for f in os.listdir(input_folder)
        if f.lower().endswith(valid_extensions)
    ]
    file_list.sort()  # Optional: sort files alphabetically

    for file_name in file_list:
        input_path = os.path.join(input_folder, file_name)
        image = cv2.imread(input_path)

        if image is None:
            print(f"[WARNING] Could not read {file_name}. Skipping.")
            continue

        print(f"\nProcessing: {file_name}")
        print("Select multiple bounding boxes for each shorthand character.")
        print(" - Draw the box with mouse drag.")
        print(" - Press ENTER or SPACE to confirm each box.")
        print(" - Press ESC when done selecting (or to skip if no boxes).")

        # This function allows selecting multiple ROIs on the opened image window
        rois = cv2.selectROIs("Select multiple ROIs", image, 
                              fromCenter=False, showCrosshair=False)

        # Close the ROI selection window (otherwise it stays open)
        cv2.destroyWindow("Select multiple ROIs")

        if len(rois) == 0:
            print("No bounding boxes selected, skipping this file.")
            continue

        # For each bounding box, crop and save
        for i, roi in enumerate(rois):
            x, y, w, h = roi
            crop = image[y:y+h, x:x+w]

            # Resize the crop to the specified dimensions
            resized_crop = cv2.resize(crop, (width, height), interpolation=cv2.INTER_AREA)

            # Build a save path: originalFileName_cropIndex.ext
            base_name, ext = os.path.splitext(file_name)
            out_filename = f"{base_name}_crop_{i}{ext}"
            out_path = os.path.join(output_folder, out_filename)

            cv2.imwrite(out_path, resized_crop)
            print(f"  Saved crop #{i} -> {out_path}")

    print("\nAll done! Multiple bounding boxes were cropped and saved.")

def main():
    parser = argparse.ArgumentParser(description="Multi-ROI Cropping Tool")
    parser.add_argument("--input", required=True,
                        help="Path to the folder of input images.")
    parser.add_argument("--output", required=True,
                        help="Path to the output folder for cropped images.")
    parser.add_argument("--width", type=int, default=128,
                        help="Target width of each cropped/resized image. Default=128.")
    parser.add_argument("--height", type=int, default=128,
                        help="Target height of each cropped/resized image. Default=128.")
    args = parser.parse_args()

    multi_crop(args.input, args.output, args.width, args.height)

if __name__ == "__main__":
    main()