import gradio as gr
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64


class ZypherChroniclesApp:
    def __init__(self):
        self.key = RSA.generate(2048)
        self.public_key = self.key.publickey()
        self.information_store = {}

    def store_information(self, key, value):
        if key and value:
            cipher = PKCS1_OAEP.new(self.public_key)
            encrypted = cipher.encrypt(value.encode())
            self.information_store[key] = base64.b64encode(encrypted).decode()
            return f"Information stored securely under key: {key}"
        else:
            return "Error: Both key and value must be provided."

    def retrieve_information(self, key):
        if key in self.information_store:
            cipher = PKCS1_OAEP.new(self.key)
            decrypted = cipher.decrypt(base64.b64decode(self.information_store[key]))
            return f"Retrieved information: {decrypted.decode()}"
        else:
            return f"Error: Key '{key}' not found."

    def view_all_keys(self):
        if self.information_store:
            return "Stored keys:\n" + "\n".join(self.information_store.keys())
        else:
            return "No keys stored yet."


def create_gradio_interface():
    app = ZypherChroniclesApp()

    with gr.Blocks(theme=gr.themes.Soft()) as interface:
        gr.Markdown(
            """
        # The Zypher Chronicles
        Welcome to Spartus, Theseus! Use this application to securely store and retrieve information,
        protecting it from Kronos' threat.
        """
        )

        with gr.Tab("Store Information"):
            store_key = gr.Textbox(label="Key")
            store_value = gr.Textbox(label="Information to Store")
            store_button = gr.Button("Store Information")
            store_output = gr.Textbox(label="Result")

            store_button.click(
                fn=app.store_information,
                inputs=[store_key, store_value],
                outputs=store_output,
            )

        with gr.Tab("Retrieve Information"):
            retrieve_key = gr.Textbox(label="Key")
            retrieve_button = gr.Button("Retrieve Information")
            retrieve_output = gr.Textbox(label="Retrieved Information")

            retrieve_button.click(
                fn=app.retrieve_information,
                inputs=retrieve_key,
                outputs=retrieve_output,
            )

        with gr.Tab("View All Keys"):
            view_button = gr.Button("View All Keys")
            view_output = gr.Textbox(label="Stored Keys")

            view_button.click(fn=app.view_all_keys, inputs=None, outputs=view_output)

    return interface


if __name__ == "__main__":
    interface = create_gradio_interface()
    interface.launch()
