{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": []
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "code",
      "source": [
        "!apt install tesseract-ocr\n",
        "!pip install pytesseract\n",
        "!apt install tesseract-ocr-fra"
      ],
      "metadata": {
        "id": "Nf6d-mfl6o9K"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "BILAN ARRETE\n"
      ],
      "metadata": {
        "id": "Gh24CD7G6dkQ"
      }
    },
    {
      "cell_type": "markdown",
      "source": [
        "Division de l'image sur 2"
      ],
      "metadata": {
        "id": "nGcXDinf6jbL"
      }
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "2Sv-cc8W6U0C",
        "outputId": "095267de-d2bc-40cd-d810-cd24669f250f"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Partie gauche enregistrée à: image007_left.png\n",
            "Partie droite enregistrée à: image007_right.png\n"
          ]
        }
      ],
      "source": [
        "from PIL import Image\n",
        "\n",
        "# Charger l'image\n",
        "image_path = \"image007.png\"\n",
        "image = Image.open(image_path)\n",
        "\n",
        "# Diviser l'image en deux parties verticalement\n",
        "width, height = image.size\n",
        "left_part = image.crop((0, 0, width // 2, height))\n",
        "right_part = image.crop((width // 2, 0, width, height))\n",
        "\n",
        "# Enregistrer les deux parties\n",
        "left_part_path = \"image007_left.png\"\n",
        "right_part_path = \"image007_right.png\"\n",
        "left_part.save(left_part_path)\n",
        "right_part.save(right_part_path)\n",
        "\n",
        "print(f\"Partie gauche enregistrée à: {left_part_path}\")\n",
        "print(f\"Partie droite enregistrée à: {right_part_path}\")\n"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "Extraction des totaux des actifs"
      ],
      "metadata": {
        "id": "xo4m26kA7Aoc"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "from PIL import Image, ImageEnhance\n",
        "import pytesseract\n",
        "import re\n",
        "\n",
        "# Définir la fonction pour traiter l'image et extraire le texte\n",
        "def process_image_and_extract_text(image_path):\n",
        "    # Charger l'image\n",
        "    image = Image.open(image_path)\n",
        "\n",
        "    # Convertir l'image en niveaux de gris\n",
        "    gray_image = image.convert('L')\n",
        "\n",
        "    # Augmenter le contraste de l'image\n",
        "    enhancer = ImageEnhance.Contrast(gray_image)\n",
        "    contrasted_image = enhancer.enhance(1.5)  # Augmenter le contraste par un facteur de 2\n",
        "\n",
        "    # Redimensionner l'image (facteur de 1.5)\n",
        "    width, height = contrasted_image.size\n",
        "    resized_image = contrasted_image.resize((int(width * 4.32), int(height * 4.32)), Image.LANCZOS)\n",
        "\n",
        "    # Binariser l'image (seuil ajusté)\n",
        "    binarized_image = resized_image.point(lambda x: 0 if x < 140 else 255, '1')\n",
        "\n",
        "    # Extraire le texte de l'image améliorée avec l'option psm 6\n",
        "    custom_config = r'--oem 3 --psm 6'\n",
        "    texte_bilan_enhanced = pytesseract.image_to_string(binarized_image, config=custom_config)\n",
        "\n",
        "\n",
        "    return texte_bilan_enhanced\n",
        "\n",
        "# Exemple de chemin d'image\n",
        "chemin_image = \"image007_left.png\"\n",
        "\n",
        "# Extraire le texte de l'image\n",
        "texte_bilan_enhanced_actifs = process_image_and_extract_text(chemin_image)\n",
        "\n",
        "# Corriger les mots incorrects\n",
        "# texte_bilan_enhanced_actifs = re.sub(r'\\bTotel\\b', 'Total', texte_bilan_enhanced_actifs, flags=re.IGNORECASE)\n",
        "# texte_bilan_enhanced_actifs = re.sub(r'\\bCouraats\\b', 'Courants', texte_bilan_enhanced_actifs, flags=re.IGNORECASE)\n",
        "# texte_bilan_enhanced_actifs = re.sub(r'\\bInomobilisés\\b', 'Immobilisés', texte_bilan_enhanced_actifs, flags=re.IGNORECASE)\n",
        "\n",
        "# Fonction pour insérer le séparateur entre les deux valeurs\n",
        "def insert_separator(line):\n",
        "    # Expression régulière pour trouver les nombres\n",
        "    numbers = re.findall(r'\\d{1,3}(?:[\\s.,]\\d{3})*', line)\n",
        "    if len(numbers) == 2:\n",
        "        # Remplacer la première occurrence du deuxième nombre par '| <number>'\n",
        "        line = re.sub(re.escape(numbers[1]), '| ' + numbers[1], line, 1)\n",
        "    return line\n",
        "\n",
        "\n",
        "def contains_keywords(text, keywords):\n",
        "    \"\"\"Check if the extracted text contains any of the specified keywords.\"\"\"\n",
        "    for keyword in keywords:\n",
        "        if keyword.lower() in text.lower():\n",
        "            return True\n",
        "    return False\n",
        "def extract_financial_data(text, keywords):\n",
        "    \"\"\"Extract financial data if the text contains specific keywords.\"\"\"\n",
        "    if contains_keywords(text, keywords):\n",
        "                return \"Il s'agit bien d'un bilan comptable:\"\n",
        "    else:\n",
        "        return \"The image does not appear to be a balance sheet.\"\n",
        "\n",
        "# Filtrer les lignes pour ne conserver que celles contenant \"Total\", \"total\" ou \"TOTAL\"\n",
        "lignes = texte_bilan_enhanced_actifs.split('\\n')\n",
        "# Filtrage des lignes selon les critères spécifiés\n",
        "pattern = re.compile(r'\\bTotal\\b|31[\\/\\-. ](12|décembre|decembre)[\\/\\-. ]20\\d{2}', re.IGNORECASE)\n",
        "\n",
        "# Appliquer le filtre et insérer les séparateurs\n",
        "lignes_filtrees = [insert_separator(ligne) for ligne in lignes if re.search(pattern, ligne)]\n",
        "\n",
        "# Rejoindre les lignes filtrées en un seul texte\n",
        "texte_filtre_actifs = '\\n'.join(lignes_filtrees)\n",
        "\n",
        "keywords = [\"Actifs\", \"Passifs\", \"Capitaux propres\", \"Résultat\", \"ETAT DE RESULTAT\"]\n",
        "extracted_value = extract_financial_data(texte_filtre_actifs, keywords)\n",
        "\n",
        "texte_filtre_actifs = re.sub(r'\\bpo\\b', '', texte_filtre_actifs)\n",
        "\n",
        "# Afficher le texte filtré et s'il 'sagit d'un bilan ou pas\n",
        "print(extracted_value)\n",
        "print(texte_filtre_actifs)\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "4nk9ylno7C3L",
        "outputId": "6870953a-059e-447a-e11a-0711d8c9672c"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Il s'agit bien d'un bilan comptable:\n",
            "BILAN ARRETE AU 31/12/2022\n",
            "31/12/2022 31/12/2021\n",
            "Total des Actifs Immobilisés 10 252 069 | 11 338 516\n",
            "Total des Actifs non Courants 10 252 069 | 11 338 516\n",
            "Total des Actifs Courants 47 017 145 | 25 782 633\n",
            "TOTAL DES ACTIFS  57 269 214 | 37 121 148\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "Extraction des totaux des passifs et des capitaux propres pour l'image007"
      ],
      "metadata": {
        "id": "TRcAZu0g7HaV"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "from PIL import Image, ImageEnhance\n",
        "import pytesseract\n",
        "\n",
        "# Définir la fonction pour traiter l'image et extraire le texte\n",
        "def process_image_and_extract_text(image_path):\n",
        "    # Charger l'image\n",
        "    image = Image.open(image_path)\n",
        "\n",
        "    # Convertir l'image en niveaux de gris\n",
        "    gray_image = image.convert('L')\n",
        "\n",
        "    # Augmenter le contraste de l'image\n",
        "    enhancer = ImageEnhance.Contrast(gray_image)\n",
        "    contrasted_image = enhancer.enhance(1)  # Augmenter le contraste par un facteur de 2\n",
        "\n",
        "    # Redimensionner l'image (facteur de 1.5)\n",
        "    width, height = contrasted_image.size\n",
        "    resized_image = contrasted_image.resize((int(width * 3.2), int(height * 3.2)), Image.LANCZOS)\n",
        "\n",
        "    # Binariser l'image (seuil ajusté)\n",
        "    binarized_image = resized_image.point(lambda x: 0 if x < 140 else 255, '1')\n",
        "\n",
        "    # Extraire le texte de l'image améliorée avec l'option psm 6\n",
        "    custom_config = r'--oem 3 --psm 6'\n",
        "    texte_bilan_enhanced = pytesseract.image_to_string(binarized_image, config=custom_config)\n",
        "\n",
        "\n",
        "    return texte_bilan_enhanced\n",
        "\n",
        "# Exemple de chemin d'image\n",
        "chemin_image = \"image007_right.png\"\n",
        "\n",
        "# Extraire le texte de l'image\n",
        "texte_bilan_enhanced_passifs = process_image_and_extract_text(chemin_image)\n",
        "\n",
        "# Fonction pour insérer le séparateur entre les deux valeurs\n",
        "def insert_separator(line):\n",
        "    # Expression régulière pour trouver les nombres\n",
        "    numbers = re.findall(r'\\d{1,3}(?:[\\s.,]\\d{3})*', line)\n",
        "    if len(numbers) == 2:\n",
        "        # Remplacer la première occurrence du deuxième nombre par '| <number>'\n",
        "        line = re.sub(re.escape(numbers[1]), '| ' + numbers[1], line, 1)\n",
        "    return line\n",
        "\n",
        "def contains_keywords(text, keywords):\n",
        "    \"\"\"Check if the extracted text contains any of the specified keywords.\"\"\"\n",
        "    for keyword in keywords:\n",
        "        if keyword.lower() in text.lower():\n",
        "            return True\n",
        "    return False\n",
        "def extract_financial_data(text, keywords):\n",
        "    \"\"\"Extract financial data if the text contains specific keywords.\"\"\"\n",
        "    if contains_keywords(text, keywords):\n",
        "                return \"Il s'agit bien d'un bilan comptable:\"\n",
        "    else:\n",
        "        return \"The image does not appear to be a balance sheet.\"\n",
        "\n",
        "# Filtrer les lignes pour ne conserver que celles contenant \"Total\", \"total\" ou \"TOTAL\"\n",
        "lignes = texte_bilan_enhanced_passifs.split('\\n')\n",
        "# Filtrage des lignes selon les critères spécifiés\n",
        "pattern = re.compile(r'\\bTotal\\b|31[\\/\\-. ](12|décembre|decembre)[\\/\\-. ]20\\d{2}', re.IGNORECASE)\n",
        "\n",
        "# Appliquer le filtre et insérer les séparateurs\n",
        "lignes_filtrees = [insert_separator(ligne) for ligne in lignes if re.search(pattern, ligne)]\n",
        "\n",
        "# Rejoindre les lignes filtrées en un seul texte\n",
        "texte_filtre_passifs = '\\n'.join(lignes_filtrees)\n",
        "\n",
        "texte_filtre_passifs = re.sub(r'\\[', '', texte_filtre_passifs)\n",
        "texte_filtre_passifs = re.sub(r'\\-', '', texte_filtre_passifs)\n",
        "texte_filtre_passifs = re.sub(r'N12  10 085 140', 'N12   10 085 140 |', texte_filtre_passifs)\n",
        "texte_filtre_passifs = re.sub(r'J', '|', texte_filtre_passifs)\n",
        "\n",
        "\n",
        "keywords = [\"Actifs\", \"Passifs\", \"Capitaux propres\", \"Résultat\", \"ETAT DE RESULTAT\"]\n",
        "extracted_value = extract_financial_data(texte_filtre_passifs, keywords)\n",
        "\n",
        "# Afficher le texte filtré et s'il 'sagit d'un bilan ou pas\n",
        "print(extracted_value)\n",
        "print(texte_filtre_passifs)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "iKdt4yup7EHH",
        "outputId": "d8108543-7db9-4749-eda4-f14f74c238e0"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Il s'agit bien d'un bilan comptable:\n",
            "BILAN ARRETE AU 31/12/2022\n",
            "31/12/2022 31/12/2021\n",
            "Total CP avant résultat de l'exercice N12   10 085 140 |  10 716 285\n",
            "Total des Capitaux Propres avant affectation N13  6 368 586 |  10 085 140\n",
            "Total des Passifs non Courants 1 885 454 | 1 058 590\n",
            "Total des Passifs Courants 61 752 346 | 46 147 699\n",
            "Total des Passifs 63 637 800 | 47 206 289\n",
            "TOTAL DES CAPITAUX PROPRES & DES PASSIFS | 57 269 214 | 37 121 148\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "Bilan 2022 exple 1"
      ],
      "metadata": {
        "id": "UQhnYBzf7P5k"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "!pip install pytesseract Pillow PyMuPDF"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "qBEDgAdL7JpB",
        "outputId": "07528575-548b-435d-e280-09a29b718a01"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Requirement already satisfied: pytesseract in /usr/local/lib/python3.10/dist-packages (0.3.10)\n",
            "Requirement already satisfied: Pillow in /usr/local/lib/python3.10/dist-packages (9.4.0)\n",
            "Collecting PyMuPDF\n",
            "  Downloading PyMuPDF-1.24.7-cp310-none-manylinux2014_x86_64.whl (3.5 MB)\n",
            "\u001b[2K     \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m3.5/3.5 MB\u001b[0m \u001b[31m14.3 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25hRequirement already satisfied: packaging>=21.3 in /usr/local/lib/python3.10/dist-packages (from pytesseract) (24.1)\n",
            "Collecting PyMuPDFb==1.24.6 (from PyMuPDF)\n",
            "  Downloading PyMuPDFb-1.24.6-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (15.7 MB)\n",
            "\u001b[2K     \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m15.7/15.7 MB\u001b[0m \u001b[31m53.3 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25hInstalling collected packages: PyMuPDFb, PyMuPDF\n",
            "Successfully installed PyMuPDF-1.24.7 PyMuPDFb-1.24.6\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "Convertir le fichier pdf en images png"
      ],
      "metadata": {
        "id": "gMulYpQB7Ubu"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "import fitz  # PyMuPDF\n",
        "from PIL import Image\n",
        "\n",
        "# Chemin vers le fichier PDF\n",
        "chemin_pdf = \"/content/bilan_2022.pdf\"\n",
        "\n",
        "# Ouvrir le fichier PDF\n",
        "pdf_document = fitz.open(chemin_pdf)\n",
        "\n",
        "# Définir une résolution DPI pour le rendu des pages\n",
        "dpi = 300\n",
        "\n",
        "# Parcourir les pages du PDF et les convertir en images PNG\n",
        "for page_num in range(len(pdf_document)):\n",
        "    page = pdf_document[page_num]\n",
        "\n",
        "    # Rendre la page en tant qu'image (pixmap)\n",
        "    zoom = dpi / 72  # 72 DPI est la résolution de base\n",
        "    mat = fitz.Matrix(zoom, zoom)\n",
        "    pix = page.get_pixmap(matrix=mat, alpha=False)\n",
        "\n",
        "    # Convertir le pixmap en une image PIL\n",
        "    image = Image.frombytes(\"RGB\", [pix.width, pix.height], pix.samples)\n",
        "\n",
        "    # Enregistrer l'image en tant que fichier PNG\n",
        "    output_path = f\"page_{page_num + 1}_bilan_2022_exple1.png\"\n",
        "    image.save(output_path, \"PNG\")\n",
        "    print(f\"Image de la page {page_num + 1} sauvegardée: {output_path}\")\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "CFxirBuS7SFC",
        "outputId": "ab83cd2f-e5a2-49b7-dad3-2915e8ff777e"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Image de la page 1 sauvegardée: page_1_bilan_2022_exple1.png\n",
            "Image de la page 2 sauvegardée: page_2_bilan_2022_exple1.png\n",
            "Image de la page 3 sauvegardée: page_3_bilan_2022_exple1.png\n",
            "Image de la page 4 sauvegardée: page_4_bilan_2022_exple1.png\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "Extraction des totaux des actifs pour l'exemple 1"
      ],
      "metadata": {
        "id": "CxUhUPtO7es2"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "from PIL import Image, ImageEnhance\n",
        "import pytesseract\n",
        "import re\n",
        "\n",
        "# Définir la fonction pour traiter l'image et extraire le texte\n",
        "def process_image_and_extract_text(image_path):\n",
        "    # Charger l'image\n",
        "    image = Image.open(image_path)\n",
        "\n",
        "    # Convertir l'image en niveaux de gris\n",
        "    gray_image = image.convert('L')\n",
        "\n",
        "    # Augmenter le contraste de l'image\n",
        "    enhancer = ImageEnhance.Contrast(gray_image)\n",
        "    contrasted_image = enhancer.enhance(1)  # Augmenter le contraste par un facteur de 2\n",
        "\n",
        "    # Redimensionner l'image (facteur de 1.5)\n",
        "    width, height = contrasted_image.size\n",
        "    resized_image = contrasted_image.resize((int(width * 8.3), int(height * 8.3)), Image.LANCZOS)\n",
        "\n",
        "    # Binariser l'image (seuil ajusté)\n",
        "    binarized_image = resized_image.point(lambda x: 0 if x < 140 else 255, '1')\n",
        "\n",
        "    # Extraire le texte de l'image améliorée avec l'option psm 6\n",
        "    custom_config = r'--oem 3 --psm 6'\n",
        "    texte_bilan_enhanced = pytesseract.image_to_string(binarized_image, config=custom_config)\n",
        "\n",
        "    return texte_bilan_enhanced\n",
        "\n",
        "# Exemple de chemin d'image\n",
        "chemin_image = \"/content/page_1_bilan_2022_exple1.png\"\n",
        "\n",
        "# Extraire le texte de l'image\n",
        "texte_bilan_enhanced = process_image_and_extract_text(chemin_image)\n",
        "\n",
        "# Fonction pour insérer le séparateur entre les deux valeurs\n",
        "def insert_separator(line):\n",
        "    # Expression régulière pour trouver les nombres\n",
        "    numbers = re.findall(r'\\d{1,3}(?:[\\s.,]\\d{3})*', line)\n",
        "    if len(numbers) == 2:\n",
        "        # Remplacer la première occurrence du deuxième nombre par '| <number>'\n",
        "        line = re.sub(re.escape(numbers[1]), '| ' + numbers[1], line, 1)\n",
        "    return line\n",
        "\n",
        "\n",
        "def contains_keywords(text, keywords):\n",
        "    \"\"\"Check if the extracted text contains any of the specified keywords.\"\"\"\n",
        "    for keyword in keywords:\n",
        "        if keyword.lower() in text.lower():\n",
        "            return True\n",
        "    return False\n",
        "def extract_financial_data(text, keywords):\n",
        "    \"\"\"Extract financial data if the text contains specific keywords.\"\"\"\n",
        "    if contains_keywords(text, keywords):\n",
        "                return \"Il s'agit bien d'un bilan comptable:\"\n",
        "    else:\n",
        "        return \"The image does not appear to be a balance sheet.\"\n",
        "\n",
        "# Filtrer les lignes pour ne conserver que celles contenant \"Total\", \"total\" ou \"TOTAL\"\n",
        "lignes = texte_bilan_enhanced.split('\\n')\n",
        "# Filtrage des lignes selon les critères spécifiés\n",
        "pattern = re.compile(r'\\bTotal\\b|31[\\/\\-. ](12|décembre|decembre)[\\/\\-. ]20\\d{2}', re.IGNORECASE)\n",
        "\n",
        "# Appliquer le filtre et insérer les séparateurs\n",
        "lignes_filtrees = [insert_separator(ligne) for ligne in lignes if re.search(pattern, ligne)]\n",
        "\n",
        "# Rejoindre les lignes filtrées en un seul texte\n",
        "texte_bilan_2022_1_actifs = '\\n'.join(lignes_filtrees)\n",
        "\n",
        "keywords = [\"Actifs\", \"Passifs\", \"Capitaux propres\", \"Résultat\", \"Resultat\", \"ETAT DE RESULTAT\"]\n",
        "extracted_value = extract_financial_data(texte_bilan_2022_1_actifs, keywords)\n",
        "\n",
        "# Afficher le texte filtré et s'il 'sagit d'un bilan ou pas\n",
        "print(extracted_value)\n",
        "print(texte_bilan_2022_1_actifs)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "4ynfApEh7fAi",
        "outputId": "03daa44e-e0c9-41f8-8f48-a18be8ac2193"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Il s'agit bien d'un bilan comptable:\n",
            "ARRETE AU 31 DECEMBRE 2022 :\n",
            "Total des actifs immobilisés 10777 848 11 096 473\n",
            "Total des actifs non courants 10 777 848 | 11 096 473 :\n",
            "Total des actifs courants 3 027 343 417| 9 280 :\n",
            "TOTAL DES ACTIFS 13.805 191 | 15 275 753 .\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "Extraction des totaux des capitaux propres et des passifs pour l'exemple 1"
      ],
      "metadata": {
        "id": "FSPctbVX7jpn"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "from PIL import Image, ImageEnhance\n",
        "import pytesseract\n",
        "import re\n",
        "\n",
        "# Définir la fonction pour traiter l'image et extraire le texte\n",
        "def process_image_and_extract_text(image_path):\n",
        "    # Charger l'image\n",
        "    image = Image.open(image_path)\n",
        "\n",
        "    # Convertir l'image en niveaux de gris\n",
        "    gray_image = image.convert('L')\n",
        "\n",
        "    # Augmenter le contraste de l'image\n",
        "    enhancer = ImageEnhance.Contrast(gray_image)\n",
        "    contrasted_image = enhancer.enhance(1)  # Augmenter le contraste par un facteur de 2\n",
        "\n",
        "    # Redimensionner l'image (facteur de 1.5)\n",
        "    width, height = contrasted_image.size\n",
        "    resized_image = contrasted_image.resize((int(width * 4), int(height * 4)), Image.LANCZOS)\n",
        "\n",
        "    # Binariser l'image (seuil ajusté)\n",
        "    binarized_image = resized_image.point(lambda x: 0 if x < 140 else 255, '1')\n",
        "\n",
        "    # Extraire le texte de l'image améliorée avec l'option psm 6\n",
        "    custom_config = r'--oem 3 --psm 6'\n",
        "    texte_bilan_enhanced = pytesseract.image_to_string(binarized_image, config=custom_config)\n",
        "\n",
        "    return texte_bilan_enhanced\n",
        "\n",
        "# Exemple de chemin d'image\n",
        "chemin_image = \"/content/page_2_bilan_2022_exple1.png\"\n",
        "\n",
        "# Extraire le texte de l'image\n",
        "texte_bilan_enhanced = process_image_and_extract_text(chemin_image)\n",
        "\n",
        "# Fonction pour insérer le séparateur entre les deux valeurs\n",
        "def insert_separator(line):\n",
        "    # Expression régulière pour trouver les nombres\n",
        "    numbers = re.findall(r'\\d{1,3}(?:[\\s.,]\\d{3})*', line)\n",
        "    if len(numbers) == 2:\n",
        "        # Remplacer la première occurrence du deuxième nombre par '| <number>'\n",
        "        line = re.sub(re.escape(numbers[1]), '| ' + numbers[1], line, 1)\n",
        "    return line\n",
        "\n",
        "\n",
        "def contains_keywords(text, keywords):\n",
        "    \"\"\"Check if the extracted text contains any of the specified keywords.\"\"\"\n",
        "    for keyword in keywords:\n",
        "        if keyword.lower() in text.lower():\n",
        "            return True\n",
        "    return False\n",
        "def extract_financial_data(text, keywords):\n",
        "    \"\"\"Extract financial data if the text contains specific keywords.\"\"\"\n",
        "    if contains_keywords(text, keywords):\n",
        "                return \"Il s'agit bien d'un bilan comptable:\"\n",
        "    else:\n",
        "        return \"The image does not appear to be a balance sheet.\"\n",
        "\n",
        "# Filtrer les lignes pour ne conserver que celles contenant \"Total\", \"total\" ou \"TOTAL\"\n",
        "lignes = texte_bilan_enhanced.split('\\n')\n",
        "# Filtrage des lignes selon les critères spécifiés\n",
        "pattern = re.compile(r'\\bTotal\\b|31[\\/\\-. ](12|décembre|decembre)[\\/\\-. ]20\\d{2}', re.IGNORECASE)\n",
        "\n",
        "# Appliquer le filtre et insérer les séparateurs\n",
        "lignes_filtrees = [insert_separator(ligne) for ligne in lignes if re.search(pattern, ligne)]\n",
        "\n",
        "# Rejoindre les lignes filtrées en un seul texte\n",
        "texte_bilan_2022_1_passifs = '\\n'.join(lignes_filtrees)\n",
        "# texte_bilan_2022_1_passifs = re.sub(r'a g', '0 | 0', texte_bilan_2022_1_passifs)\n",
        "\n",
        "keywords = [\"Actifs\", \"Passifs\", \"Capitaux propres\", \"Résultat\", \"ETAT DE RESULTAT\"]\n",
        "extracted_value = extract_financial_data(texte_bilan_2022_1_passifs, keywords)\n",
        "\n",
        "# Afficher le texte filtré et s'il 'sagit d'un bilan ou pas\n",
        "print(extracted_value)\n",
        "print(texte_bilan_2022_1_passifs)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "_AQX3p317j3I",
        "outputId": "727cc8c9-0941-40ed-a52e-eb667777eee9"
      },
      "execution_count": null,
      "outputs": [
        {
          "metadata": {
            "tags": null
          },
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "Il s'agit bien d'un bilan comptable:\n",
            "4 ARRETE AU 31 DECEMBRE 2022\n",
            "Total des capitaux propres avant resuiltat affectation 5 13 593 714 13 052 935\n",
            "Total des passifs non courants 177 857 |\n",
            "Total des passifs courants 211 477 | 2 104 967 :\n",
            "Total des passifs _ 211 477 | 2 222 818 :\n",
            "_ TOTAL DES CAPITAUX PROPRES ET DES PASSIFS 13 805 191 | 15 275 753 :\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "Bilan 2022 exple 2"
      ],
      "metadata": {
        "id": "S6k5YTX375Ho"
      }
    },
    {
      "cell_type": "markdown",
      "source": [
        "Convertir le fichier pdf en images png"
      ],
      "metadata": {
        "id": "dlodrMzU78MG"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "import fitz  # PyMuPDF\n",
        "from PIL import Image\n",
        "\n",
        "# Chemin vers le fichier PDF\n",
        "chemin_pdf = \"/content/bilan_2022_2.pdf\"\n",
        "\n",
        "# Ouvrir le fichier PDF\n",
        "pdf_document = fitz.open(chemin_pdf)\n",
        "\n",
        "# Définir une résolution DPI pour le rendu des pages\n",
        "dpi = 300\n",
        "\n",
        "# Parcourir les pages du PDF et les convertir en images PNG\n",
        "for page_num in range(len(pdf_document)):\n",
        "    page = pdf_document[page_num]\n",
        "\n",
        "    # Rendre la page en tant qu'image (pixmap)\n",
        "    zoom = dpi / 72  # 72 DPI est la résolution de base\n",
        "    mat = fitz.Matrix(zoom, zoom)\n",
        "    pix = page.get_pixmap(matrix=mat, alpha=False)\n",
        "\n",
        "    # Convertir le pixmap en une image PIL\n",
        "    image = Image.frombytes(\"RGB\", [pix.width, pix.height], pix.samples)\n",
        "\n",
        "    # Enregistrer l'image en tant que fichier PNG\n",
        "    output_path = f\"page_{page_num + 1}_bilan_2022_exple2.png\"\n",
        "    image.save(output_path, \"PNG\")\n",
        "    print(f\"Image de la page {page_num + 1} sauvegardée: {output_path}\")\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "_B9I95CV75hi",
        "outputId": "734dd72d-c80e-445f-9414-8d7943423f3f"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Image de la page 1 sauvegardée: page_1_bilan_2022_exple2.png\n",
            "Image de la page 2 sauvegardée: page_2_bilan_2022_exple2.png\n",
            "Image de la page 3 sauvegardée: page_3_bilan_2022_exple2.png\n",
            "Image de la page 4 sauvegardée: page_4_bilan_2022_exple2.png\n",
            "Image de la page 5 sauvegardée: page_5_bilan_2022_exple2.png\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "Extraction des totaux des actifs pour l'exemple 2"
      ],
      "metadata": {
        "id": "ZLvFlwyV8Aeu"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "from PIL import Image, ImageEnhance\n",
        "import pytesseract\n",
        "import re\n",
        "\n",
        "# Définir la fonction pour traiter l'image et extraire le texte\n",
        "def process_image_and_extract_text(image_path):\n",
        "    # Charger l'image\n",
        "    image = Image.open(image_path)\n",
        "\n",
        "    # Convertir l'image en niveaux de gris\n",
        "    gray_image = image.convert('L')\n",
        "\n",
        "    # Augmenter le contraste de l'image\n",
        "    enhancer = ImageEnhance.Contrast(gray_image)\n",
        "    contrasted_image = enhancer.enhance(2)  # Augmenter le contraste par un facteur de 2\n",
        "\n",
        "    # Redimensionner l'image (facteur de 1.5)\n",
        "    width, height = contrasted_image.size\n",
        "    resized_image = contrasted_image.resize((int(width * 3), int(height * 3)), Image.LANCZOS)\n",
        "\n",
        "    # Binariser l'image (seuil ajusté)\n",
        "    binarized_image = resized_image.point(lambda x: 0 if x < 140 else 255, '1')\n",
        "\n",
        "    # Extraire le texte de l'image améliorée avec l'option psm 6\n",
        "    custom_config = r'--oem 3 --psm 6'\n",
        "    texte_bilan_enhanced = pytesseract.image_to_string(binarized_image, config=custom_config)\n",
        "\n",
        "    return texte_bilan_enhanced\n",
        "\n",
        "# Exemple de chemin d'image\n",
        "chemin_image = \"/content/page_2_bilan_2022_exple2.png\"\n",
        "\n",
        "# Extraire le texte de l'image\n",
        "texte_bilan_enhanced = process_image_and_extract_text(chemin_image)\n",
        "\n",
        "# Fonction pour insérer le séparateur entre les deux valeurs\n",
        "def insert_separator(line):\n",
        "    # Expression régulière pour trouver les nombres\n",
        "    numbers = re.findall(r'\\d{1,3}(?:[\\s.,]\\d{3})*', line)\n",
        "    if len(numbers) == 2:\n",
        "        # Remplacer la première occurrence du deuxième nombre par '| <number>'\n",
        "        line = re.sub(re.escape(numbers[1]), '| ' + numbers[1], line, 1)\n",
        "    return line\n",
        "\n",
        "\n",
        "def contains_keywords(text, keywords):\n",
        "    \"\"\"Check if the extracted text contains any of the specified keywords.\"\"\"\n",
        "    for keyword in keywords:\n",
        "        if keyword.lower() in text.lower():\n",
        "            return True\n",
        "    return False\n",
        "def extract_financial_data(text, keywords):\n",
        "    \"\"\"Extract financial data if the text contains specific keywords.\"\"\"\n",
        "    if contains_keywords(text, keywords):\n",
        "                return \"Il s'agit bien d'un bilan comptable:\"\n",
        "    else:\n",
        "        return \"The image does not appear to be a balance sheet.\"\n",
        "\n",
        "# Filtrer les lignes pour ne conserver que celles contenant \"Total\", \"total\" ou \"TOTAL\"\n",
        "lignes = texte_bilan_enhanced.split('\\n')\n",
        "# Filtrage des lignes selon les critères spécifiés\n",
        "pattern = re.compile(r'\\bTotal\\b|31[\\/\\-. ](12|décembre|decembre)[\\/\\-. ]20\\d{2}', re.IGNORECASE)\n",
        "\n",
        "# Appliquer le filtre et insérer les séparateurs\n",
        "lignes_filtrees = [insert_separator(ligne) for ligne in lignes if re.search(pattern, ligne)]\n",
        "\n",
        "# Rejoindre les lignes filtrées en un seul texte\n",
        "texte_bilan_2022_2_actifs = '\\n'.join(lignes_filtrees)\n",
        "texte_bilan_2022_2_actifs = re.sub(r'\\~', '', texte_bilan_2022_2_actifs)\n",
        "texte_bilan_2022_2_actifs = re.sub(r'\\-', '', texte_bilan_2022_2_actifs)\n",
        "texte_bilan_2022_2_actifs = re.sub(r'\\(', '', texte_bilan_2022_2_actifs)\n",
        "texte_bilan_2022_2_actifs = re.sub(r'\\_', '', texte_bilan_2022_2_actifs)\n",
        "\n",
        "\n",
        "keywords = [\"Actifs\", \"Passifs\", \"Capitaux propres\", \"Résultat\", \"ETAT DE RESULTAT\"]\n",
        "extracted_value = extract_financial_data(texte_bilan_2022_2_actifs, keywords)\n",
        "\n",
        "# Afficher le texte filtré et s'il 'sagit d'un bilan ou pas\n",
        "print(extracted_value)\n",
        "print(texte_bilan_2022_2_actifs)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "_xb0Bhlc7948",
        "outputId": "302a666d-0753-4b04-8a0d-9c1e56575043"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Il s'agit bien d'un bilan comptable:\n",
            "| Actifs Notes 31.12.2022 31.12.2021\n",
            " Total des actifs immohilisés 13 411 516 | 13 694 454\n",
            "Total des actifs non courants 13 418 313 | 13 705 529\n",
            " Total des actifs courants 3 305 096 | 4 094 239\n",
            " Total des actifs 16 723409 17799 768\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "Extraction des totaux des capitaux propres et des passifs pour l'exemple 2"
      ],
      "metadata": {
        "id": "oxAy8oTT8Gvo"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "from PIL import Image, ImageEnhance\n",
        "import pytesseract\n",
        "import re\n",
        "\n",
        "# Définir la fonction pour traiter l'image et extraire le texte\n",
        "def process_image_and_extract_text(image_path):\n",
        "    # Charger l'image\n",
        "    image = Image.open(image_path)\n",
        "\n",
        "    # Convertir l'image en niveaux de gris\n",
        "    gray_image = image.convert('L')\n",
        "\n",
        "    # Augmenter le contraste de l'image\n",
        "    enhancer = ImageEnhance.Contrast(gray_image)\n",
        "    contrasted_image = enhancer.enhance(2)  # Augmenter le contraste par un facteur de 2\n",
        "\n",
        "    # Redimensionner l'image (facteur de 1.5)\n",
        "    width, height = contrasted_image.size\n",
        "    resized_image = contrasted_image.resize((int(width * 3), int(height * 3)), Image.LANCZOS)\n",
        "\n",
        "    # Binariser l'image (seuil ajusté)\n",
        "    binarized_image = resized_image.point(lambda x: 0 if x < 140 else 255, '1')\n",
        "\n",
        "    # Extraire le texte de l'image améliorée avec l'option psm 6\n",
        "    custom_config = r'--oem 3 --psm 6'\n",
        "    texte_bilan_enhanced = pytesseract.image_to_string(binarized_image, config=custom_config)\n",
        "\n",
        "    return texte_bilan_enhanced\n",
        "\n",
        "# Exemple de chemin d'image\n",
        "chemin_image = \"/content/page_3_bilan_2022_exple2.png\"\n",
        "\n",
        "# Extraire le texte de l'image\n",
        "texte_bilan_enhanced = process_image_and_extract_text(chemin_image)\n",
        "\n",
        "# Fonction pour insérer le séparateur entre les deux valeurs\n",
        "def insert_separator(line):\n",
        "    # Expression régulière pour trouver les nombres\n",
        "    numbers = re.findall(r'\\d{1,3}(?:[\\s.,]\\d{3})*', line)\n",
        "    if len(numbers) == 2:\n",
        "        # Remplacer la première occurrence du deuxième nombre par '| <number>'\n",
        "        line = re.sub(re.escape(numbers[1]), '| ' + numbers[1], line, 1)\n",
        "    return line\n",
        "\n",
        "def contains_keywords(text, keywords):\n",
        "    \"\"\"Check if the extracted text contains any of the specified keywords.\"\"\"\n",
        "    for keyword in keywords:\n",
        "        if keyword.lower() in text.lower():\n",
        "            return True\n",
        "    return False\n",
        "\n",
        "def extract_financial_data(text, keywords):\n",
        "    \"\"\"Extract financial data if the text contains specific keywords.\"\"\"\n",
        "    if contains_keywords(text, keywords):\n",
        "        return \"Il s'agit bien d'un bilan comptable:\"\n",
        "    else:\n",
        "        return \"The image does not appear to be a balance sheet.\"\n",
        "\n",
        "# Filtrer les lignes pour ne conserver que celles contenant \"Total\", \"total\" ou \"TOTAL\"\n",
        "lignes = texte_bilan_enhanced.split('\\n')\n",
        "# Filtrage des lignes selon les critères spécifiés\n",
        "pattern = re.compile(r'\\bTotal\\b|31[\\/\\-. ](12|décembre|decembre)[\\/\\-. ]20\\d{2}', re.IGNORECASE)\n",
        "\n",
        "# Appliquer le filtre et insérer les séparateurs\n",
        "lignes_filtrees = [insert_separator(ligne) for ligne in lignes if re.search(pattern, ligne)]\n",
        "\n",
        "# Rejoindre les lignes filtrées en un seul texte\n",
        "texte_bilan_2022_2_passifs = '\\n'.join(lignes_filtrees)\n",
        "texte_bilan_2022_2_passifs = re.sub(r'\\:', '', texte_bilan_2022_2_passifs)\n",
        "texte_bilan_2022_2_passifs = re.sub(r'7 ', '', texte_bilan_2022_2_passifs)\n",
        "# texte_bilan_2022_2_passifs = re.sub(r'| Total', 'Total', texte_bilan_2022_2_passifs)\n",
        "texte_bilan_2022_2_passifs = re.sub(r'a g', '0 | 0', texte_bilan_2022_2_passifs)\n",
        "\n",
        "keywords = [\"Actifs\", \"Passifs\", \"Capitaux propres\", \"Résultat\", \"ETAT DE RESULTAT\"]\n",
        "extracted_value = extract_financial_data(texte_bilan_2022_2_passifs, keywords)\n",
        "\n",
        "# Afficher le texte filtré et s'il 'sagit d'un bilan ou pas\n",
        "print(extracted_value)\n",
        "print(texte_bilan_2022_2_passifs)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "3ljAynrz8Bh0",
        "outputId": "d65999f0-e67c-4c50-e38b-6b21994e32d1"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Il s'agit bien d'un bilan comptable:\n",
            "L. Bilan au 31 Décembre 2022 \n",
            ". Capitaux propres et passifs Notes 31.12.2022 31.12.2021\n",
            "Total des capitaux propres avant affectation 16 360 904 | 15 716 941\n",
            "Total des passifs non courants 0 | 0\n",
            "| Total des passifs courants 362 505 | 2 082 827\n",
            "Total des passifs 362 505 | 2 082 827\n",
            " Total des capitaux propres et passifs 16 723 409 | 1799 768\n"
          ]
        }
      ]
    }
  ]
}
