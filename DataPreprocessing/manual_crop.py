import os
import cv2
import argparse

def manual_crop(input_folder, output_folder):
    """
    Opens each image in input_folder, allows user to select a bounding box,
    crops the image to that bounding box, and saves the result to output_folder.
    """

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Get all image filenames in the input folder
    filenames = [f for f in os.listdir(input_folder)
                 if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    for idx, filename in enumerate(filenames):
        input_path = os.path.join(input_folder, filename)
        img = cv2.imread(input_path)

        if img is None:
            print(f"Warning: Could not read file {filename}. Skipping.")
            continue

        # Display instructions
        print(f"\nProcessing: {filename}")
        print("  1) Draw a box around the region you want to crop.")
        print("  2) Press Enter or Space to confirm the bounding box.")
        print("  3) Press 'c' to confirm cropping.")
        print("  4) Press Escape (ESC) if you want to skip this file.\n")

        # Let user select a bounding box on the image
        # selectROI returns (x, y, w, h)
        roi = cv2.selectROI("Select ROI (Press ENTER or SPACE when done)", img, False, False)

        # If ROI is all zeros, it means user hit ESC or canceled
        if roi == (0, 0, 0, 0):
            print(f"Skipping {filename} (no ROI selected).")
            cv2.destroyWindow("Select ROI (Press ENTER or SPACE when done)")
            continue

        x, y, w, h = roi
        # Crop the selected region
        cropped_img = img[y:y+h, x:x+w]

        # Display the cropped image in a new window for final confirmation
        cv2.imshow("Cropped Preview (Press 'c' to confirm, ESC to skip)", cropped_img)

        key = cv2.waitKey(0)
        if key == 99:  # ASCII code for 'c'
            # Save the cropped result
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, cropped_img)
            print(f"Saved cropped image to {output_path}")
        else:
            print(f"Skipping save for {filename}")

        # Close the preview windows
        cv2.destroyAllWindows()

    print("\nAll done! Cropping complete.")


def main():
    parser = argparse.ArgumentParser(description="Manual Cropping Tool")
    parser.add_argument("--input", required=True, help="Path to the input folder of images.")
    parser.add_argument("--output", required=True, help="Path to the output folder to save cropped images.")
    args = parser.parse_args()

    manual_crop(args.input, args.output)


if __name__ == "__main__":
    main()