import gradio as gr
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import os


class ZypherChroniclesApp:
    def __init__(self):
        self.key = RSA.generate(2048)
        self.public_key = self.key.publickey()
        self.information_store = {}

    # thus is to store files in the server securely
    def store_file(self, file, key):
        if file is None:
            return "Error: No file is being uploaded."
        if not key:
            return "Error: Key must be provided to continue."
        try:
            # Read the content of the file
            content = file.read()
            if isinstance(content, str):
                content = content.encode()

            # Encrypt the content in chunks due to RSA size limitations
            cipher = PKCS1_OAEP.new(self.public_key)
            chunk_size = 190  # Maximum size for 2048-bit key
            encrypted = b""
            for i in range(0, len(content), chunk_size):
                chunk = content[i : i + chunk_size]
                encrypted += cipher.encrypt(chunk)

            # Save the encrypted content
            filename = f"{key}_encrypted.bin"
            with open(filename, "wb") as f:
                f.write(encrypted)
            return f"File encrypted and stored as {filename}"
        except Exception as e:
            return f"Error occurred: {str(e)}"

    def retrieve_file(self, key):
        filename = f"{key}_encrypted.bin"
        if not os.path.exists(filename):
            return None, f"Error: No file found for key '{key}'"

        try:
            with open(filename, "rb") as f:
                encrypted = f.read()

            cipher = PKCS1_OAEP.new(self.key)
            decrypted = cipher.decrypt(encrypted)

            output_filename = f"{key}_decrypted.txt"
            with open(output_filename, "wb") as f:
                f.write(decrypted)

            return output_filename, f"File decrypted and saved as {output_filename}"
        except Exception as e:
            return None, f"Error occurred: {str(e)}"

    def view_all_keys(self):
        files = [f.split("_")[0] for f in os.listdir() if f.endswith("_encrypted.bin")]
        if files:
            return "Stored keys:\n" + "\n".join(files)
        else:
            return "No keys stored yet."


def create_gradio_interface():
    app = ZypherChroniclesApp()

    with gr.Blocks(theme=gr.themes.Soft()) as interface:
        gr.Markdown(
            """
        # The Zypher Chronicles
        Welcome to Spartus, Theseus! Use this application to securely store and retrieve files,
        protecting them from Kronos' threat.
        """
        )

        with gr.Tab("Store File"):
            store_file = gr.File(label="File to Encrypt")
            store_key = gr.Textbox(label="Key")
            store_button = gr.Button("Store File")
            store_output = gr.Textbox(label="Result")

            store_button.click(
                fn=app.store_file, inputs=[store_file, store_key], outputs=store_output
            )

        with gr.Tab("Retrieve File"):
            retrieve_key = gr.Textbox(label="Key")
            retrieve_button = gr.Button("Retrieve File")
            retrieve_output = gr.Textbox(label="Result")
            retrieved_file = gr.File(label="Retrieved File")

            retrieve_button.click(
                fn=app.retrieve_file,
                inputs=retrieve_key,
                outputs=[retrieved_file, retrieve_output],
            )

        with gr.Tab("View All Keys"):
            view_button = gr.Button("View All Keys")
            view_output = gr.Textbox(label="Stored Keys")

            view_button.click(fn=app.view_all_keys, inputs=None, outputs=view_output)

    return interface


if __name__ == "__main__":
    interface = create_gradio_interface()
    interface.launch()
