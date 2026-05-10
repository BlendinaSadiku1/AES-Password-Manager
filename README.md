# AES-Password-Manager

AES Password Manager është një aplikacion i thjeshtë në Python për ruajtjen dhe menaxhimin e fjalëkalimeve në mënyrë më të sigurt. Projekti përdor enkriptim AES për mbrojtjen e fjalëkalimeve dhe databazë për ruajtjen e të dhënave.

## Qëllimi i projektit

Qëllimi i këtij projekti është krijimi i një Password Manager-i ku përdoruesi mund të ruajë fjalëkalimet e llogarive të ndryshme në formë të enkriptuar, në vend që ato të ruhen si tekst i thjeshtë.

## Funksionalitetet kryesore

- Gjenerimi i fjalëkalimeve të sigurta
- Ruajtja e fjalëkalimeve në databazë
- Enkriptimi i fjalëkalimeve me AES
- Dekriptimi i fjalëkalimeve kur nevojiten
- Organizimi i fjalëkalimeve sipas llogarisë/kategorisë
- Lidhja me databazë përmes Python

## Teknologjitë e përdorura

Python – për logjikën e aplikacionit
Tkinter – për ndërtimin e GUI-së
MySQL – për ruajtjen e të dhënave
mysql-connector-python – për lidhjen me databazën
cryptography – për AES encryption dhe hashing

## Struktura e projektit

main.py – përmban GUI-në dhe logjikën kryesore të aplikacionit
database.py – menaxhon lidhjen me databazën dhe funksionet për userat
crypto_utils.py – përmban funksionet për hashing, AES encryption dhe decryption
password_generator.py – gjeneron fjalëkalime të sigurta
db_config.py – përmban konfigurimin e databazës

## Siguria

Master password-i nuk ruhet si tekst i thjeshtë në databazë. Ai ruhet si hash së bashku me një salt random për rritjen e sigurisë.

Fjalëkalimet e llogarive ruhen të enkriptuara me AES. Për çdo encryption përdoret një nonce random për të rritur sigurinë dhe për të parandaluar krijimin e ciphertext-eve identike.

## Backup dhe sinkronizim

Aplikacioni mbështet export dhe import të të dhënave përmes një sync file në format JSON. Të dhënat e backup-it ruhen të enkriptuara me AES për mbrojtje shtesë.

## Databaza

Projekti përdor dy tabela kryesore:

users
Ruajnë të dhënat e përdoruesve:
- email
- salt
- password_hash
- created_at

passwords
Ruajnë të dhënat e fjalëkalimeve:
- account
- username
- category
- encrypted_password
- nonce
- notes
- updated_at
