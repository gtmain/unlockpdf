#!/usr/bin/env python3
"""
UnlockPDF - Flask web app
Removes password protection from a PDF file when you know the password.
"""

import io
import os
from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from pypdf import PdfReader, PdfWriter
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024  # 25 MB upload limit


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/unlock", methods=["POST"])
def unlock():
    file = request.files.get("pdf_file")
    password = request.form.get("password", "")

    if not file or file.filename == "":
        flash("Please choose a PDF file.")
        return redirect(url_for("index"))

    if not file.filename.lower().endswith(".pdf"):
        flash("Please upload a .pdf file.")
        return redirect(url_for("index"))

    filename = secure_filename(file.filename)

    try:
        reader = PdfReader(file.stream)

        if reader.is_encrypted:
            if not password:
                flash("This PDF is password-protected. Please enter the password.")
                return redirect(url_for("index"))
            result = reader.decrypt(password)
            if result == 0:
                flash("Incorrect password, or the PDF could not be decrypted.")
                return redirect(url_for("index"))

        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)

        if reader.metadata:
            try:
                writer.add_metadata(reader.metadata)
            except Exception:
                pass

        output_buffer = io.BytesIO()
        writer.write(output_buffer)
        output_buffer.seek(0)

        unlocked_name = f"unlocked_{filename}"
        return send_file(
            output_buffer,
            mimetype="application/pdf",
            as_attachment=True,
            download_name=unlocked_name,
        )

    except Exception as e:
        flash(f"Error processing PDF: {e}")
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
