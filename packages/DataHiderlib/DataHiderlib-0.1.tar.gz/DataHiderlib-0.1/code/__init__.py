import file_hider
import text_hider
import cv2

class textHider:
    def encode_image(input_image,output_image,secret_data):
        encoded_image = text_hider.encode(image_name=input_image, secret_data=secret_data)
        cv2.imwrite(output_image, encoded_image)
    def decode_image(input_image):
        decoded_data = text_hider.decode(input_image)
        print("[+] Decoded data:", decoded_data)

class fileHider:
    def encode_image(input_image,output_image,input_filename,n_bits):
        secret_data = ""
        with open(input_filename, "rb") as f:
            secret_data = f.read()
        encoded_image = file_hider.encode(image_name=input_image, secret_data=secret_data, n_bits=n_bits)
        cv2.imwrite(output_image, encoded_image)
        print("[+] Saved encoded image.")
    def decode_image(input_image,file_name,n_bits):
        decoded_data = file_hider.decode(input_image,n_bits=n_bits, in_bytes=True)
        if len(decoded_data) > 100:
            with open(file_name, "wb") as f:
                f.write(decoded_data)
            print(f"[+] File decoded, {input_image} is saved successfully.")
        else:
            print("[+] Decoded data:", decoded_data)