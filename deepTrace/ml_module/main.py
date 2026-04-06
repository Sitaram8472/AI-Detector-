# from src.text.pipeline.predict_pipeline import predict
# from src.utils.helper import print_result

# if __name__ == "__main__":
#     text = input("Enter text: ")
#     result = predict(text)
#     print_result(result)


from src.text.pipeline.predict_pipeline import predict
from src.image.pipeline.predict_image import predict_image

mode = input("Enter mode (text/image): ")

if mode == "text":
    text = input("Enter text: ")
    result = predict(text)
    print(result)

elif mode == "image":
    path = input("Enter image path: ")
    result = predict_image(path)
    print("Result:", result)

# from src.text.pipeline.predict_pipeline import predict as predict_text
# from src.image.pipeline.predict_image import predict_image
# from src.image.pipeline.predict_video import predict_video


# def main():
#     print("\nSelect mode:")
#     print("1 → Text Detection")
#     print("2 → Image Detection")
#     print("3 → Video Detection")

#     choice = input("\nEnter choice (1/2/3): ").strip()
# #text
#     if choice == "1":
#         text = input("\nEnter text:\n")
#         result = predict_text(text)

#         print("\n TEXT RESULT")
#         print(result)

#    #image
#     elif choice == "2":
#         path = input("\nEnter image path: ").strip()
#         result = predict_image(path)

#         print("\n IMAGE RESULT")
#         print("Label:", result["label"])
#         print("Confidence:", result["confidence"])
# #video
#     elif choice == "3":
#         path = input("\nEnter video path: ").strip()

#         print("\n Processing video... (this may take time)")

#         result = predict_video(path, frame_skip=5)

#         print("\n VIDEO RESULT")
#         print("Label:", result["label"])
#         print("Confidence:", result["confidence"])
#         print("Frames Used:", result["frames_used"])

#     else:
#         print(" Invalid choice. Please enter 1, 2, or 3.")


# #run
# if __name__ == "__main__":
#     main()