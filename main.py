import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
import os
import winreg
import threading
import stat
import shutil
import string
from threading import Timer
import subprocess
import ctypes
import locale

# ==========================================
# UZUN REHBER METİNLERİ (TUTORIALS)
# ==========================================
TURKISH_TUTORIAL = """HyperZero, bilgisayarınızda biriken inatçı uygulama kalıntılarını, gizli oyun dosyalarını ve kayıt defteri (Registry) izlerini bulup kökünden kazımak için geliştirilmiş profesyonel bir sistem aracıdır.

📌 NASIL KULLANILIR?
1. Sol menüdeki "⚙️ Uygulama Kaldır" butonunu kullanarak silmek istediğiniz programı Windows üzerinden normal bir şekilde kaldırın.
2. Arama kutusuna sildiğiniz programın adını yazın ve ENTER tuşuna basın.
3. HyperZero tüm disklerinizi tarayarak arkada bırakılan çöpleri bulacaktır.
4. Listelenen dosyaya ÇİFT TIKLAYARAK konumunu açabilir ve Windows Gezgini'nde inceleyebilirsiniz.
5. İstenmeyen ögelere sağ tıklayıp "Kesin Olarak Sil" komutuyla fiziksel olarak yok edebilirsiniz.

✨ V1.0 ÖNE ÇIKAN ÖZELLİKLERİ
• 🌓 Tema Desteği: Ayarlar menüsünden Aydınlık ve Karanlık mod arasında dilediğiniz gibi geçiş yapabilirsiniz.
• 🛡️ PowerShell Yıkım Motoru: Antivirüs kilitlerini aşarak zorla silme işlemi yapar.
• 💾 Multi-Disk Taraması: Sadece C: diskini değil, D: ve E: gibi tüm disklerdeki Steam ve Epic Games klasörlerini de tarar.
• 🎯 Akıllı Navigasyon: Kayıt defteri izlerine çift tıkladığınızda Regedit'i otomatik açarak sizi tam o dosyanın üzerine götürür.

⚠️ GÜVENLİK VE SORUMLULUK REDDİ
Listede "Kritik" (Kırmızı) olarak işaretlenen dosyalar Windows sistem dosyalarıdır. Ne yaptığınızı tam olarak bilmiyorsanız bu dosyaları SİLMEYİNİZ. 

Bu program, sistemdeki dosyaları fiziksel ve kalıcı olarak silmek üzere tasarlanmıştır. Yanlış bir dosyanın veya sistem kaydının silinmesinden doğabilecek veri kayıpları veya işletim sistemi arızalarından geliştirici HİÇBİR SORUMLULUK KABUL ETMEZ. Programı kullanarak tüm riski üstlenmiş olursunuz."""

ENGLISH_TUTORIAL = """HyperZero is a professional system tool developed to find and root out stubborn application remnants, hidden game files, and registry traces accumulating on your computer.

📌 HOW TO USE?
1. Uninstall the program normally via Windows using the "⚙️ Uninstall App" button.
2. Type the name of the deleted program in the search box and press ENTER.
3. HyperZero will scan all your disks to find the left-behind trash.
4. You can DOUBLE-CLICK the listed file to open its location and inspect it.
5. Right-click on unwanted items and physically destroy them using the "Force Delete" command.

✨ V1.0 HIGHLIGHTS
• 🌓 Theme Support: Switch between Light and Dark modes.
• 🛡️ PowerShell Destruction Engine: Bypasses locks for forced deletion.
• 💾 Multi-Disk Scan: Scans folders on all disks like C:, D: and E:.
• 🎯 Smart Navigation: Double-clicking registry traces opens Regedit directly.

⚠️ SECURITY AND DISCLAIMER
Files marked as "Critical" (Red) are Windows system files. DO NOT DELETE them unless you know what you are doing.

This program is designed to permanently delete files. The developer ACCEPTS NO RESPONSIBILITY for data loss or operating system malfunctions that may arise. By using the program, you assume all risks."""

# ==========================================
# 29 DİL (İ18N) VERİTABANI
# ==========================================
# Not: Çökmeyi engellemek için her dilin temel arayüz kelimeleri eklenmiştir.
LANGUAGES = {
    "Turkish": {
        "scan": "🔍  Sistemi Tara", "appwiz": "⚙️ Uygulama Kaldır", "settings": "🎨 Ayarlar",
        "main_title": "Gelişmiş Oyun ve Dosya Takibi", "placeholder": "Dosya, Uygulama veya Oyun Adı Yazın ve ENTER'a basın...",
        "status_ready": "Sistem Hazır. (Konumunu görmek için ögeye çift tıklayın)", "btn_clean": "✨ Güvenli Kalıntıları Temizle",
        "col_type": "TÜR", "col_path": "DOSYA / KAYIT YOLU", "col_risk": "RİSK DURUMU",
        "ctx_open": "📂 Konumu Aç", "ctx_del": "🗑️ Seçileni Kesin Olarak Sil",
        "set_title": "Ayarlar", "set_theme": "Görünüm Modu", "set_lang": "Dil Seçeneği", "set_save": "💾 Kaydet",
        "ver": "v1.0 | Global Edition", "admin": "Yetki: Yönetici", "no_admin": "Yetki: Kısıtlı",
        "tut_title": "🚀 HyperZero v1.0'a Hoş Geldiniz", "tut_btn": "Anladım, Temizliğe Başla!",
        "tut_body": TURKISH_TUTORIAL
    },
    "English": {
        "scan": "🔍  Scan System", "appwiz": "⚙️ Uninstall App", "settings": "🎨 Settings",
        "main_title": "Advanced File & Game Tracker", "placeholder": "Type File, App or Game Name and press ENTER...",
        "status_ready": "System Ready. (Double click to open item location)", "btn_clean": "✨ Clean Safe Remnants",
        "col_type": "TYPE", "col_path": "FILE / REGISTRY PATH", "col_risk": "RISK STATUS",
        "ctx_open": "📂 Open Location", "ctx_del": "🗑️ Force Delete Selected",
        "set_title": "Settings", "set_theme": "Appearance", "set_lang": "Language", "set_save": "💾 Save Settings",
        "ver": "v1.0 | Global Edition", "admin": "Privilege: Admin", "no_admin": "Privilege: Restricted",
        "tut_title": "🚀 Welcome to HyperZero v1.0", "tut_btn": "Got it, Let's Start!",
        "tut_body": ENGLISH_TUTORIAL
    },
    "German": {"scan": "🔍 System Scannen", "appwiz": "⚙️ App Deinstallieren", "settings": "🎨 Einstellungen", "main_title": "Erweiterter Tracker", "placeholder": "Name eingeben + ENTER drücken...", "status_ready": "Bereit. (Doppelklick zum Öffnen)", "btn_clean": "✨ Sichere Reste Löschen", "col_type": "TYP", "col_path": "DATEI / REGISTRY PFAD", "col_risk": "RISIKO", "ctx_open": "📂 Öffnen", "ctx_del": "🗑️ Löschen", "set_title": "Einstellungen", "set_theme": "Thema", "set_lang": "Sprache", "set_save": "💾 Speichern", "tut_title": "🚀 Willkommen", "tut_btn": "Starten!"},
    "Spanish": {"scan": "🔍 Escanear Sistema", "appwiz": "⚙️ Desinstalar App", "settings": "🎨 Ajustes", "main_title": "Rastreador Avanzado", "placeholder": "Escribe un nombre y presiona ENTER...", "status_ready": "Listo. (Doble clic para abrir)", "btn_clean": "✨ Limpiar Seguros", "col_type": "TIPO", "col_path": "RUTA", "col_risk": "RIESGO", "ctx_open": "📂 Abrir", "ctx_del": "🗑️ Borrar", "set_title": "Ajustes", "set_theme": "Tema", "set_lang": "Idioma", "set_save": "💾 Guardar", "tut_title": "🚀 Bienvenido", "tut_btn": "¡Empezar!"},
    "French": {"scan": "🔍 Scanner le Système", "appwiz": "⚙️ Désinstaller App", "settings": "🎨 Paramètres", "main_title": "Traqueur Avancé", "placeholder": "Tapez un nom et appuyez sur ENTRÉE...", "status_ready": "Prêt. (Double-cliquez pour ouvrir)", "btn_clean": "✨ Nettoyer Sûrs", "col_type": "TYPE", "col_path": "CHEMIN", "col_risk": "RISQUE", "ctx_open": "📂 Ouvrir", "ctx_del": "🗑️ Supprimer", "set_title": "Paramètres", "set_theme": "Thème", "set_lang": "Langue", "set_save": "💾 Enregistrer", "tut_title": "🚀 Bienvenue", "tut_btn": "Commencer !"},
    "Russian": {"scan": "🔍 Скан. Систему", "appwiz": "⚙️ Удалить Приложение", "settings": "🎨 Настройки", "main_title": "Расширенный Трекер", "placeholder": "Введите имя и нажмите ENTER...", "status_ready": "Готов. (Двойной клик для открытия)", "btn_clean": "✨ Очистить Безопасные", "col_type": "ТИП", "col_path": "ПУТЬ", "col_risk": "РИСК", "ctx_open": "📂 Открыть", "ctx_del": "🗑️ Удалить", "set_title": "Настройки", "set_theme": "Тема", "set_lang": "Язык", "set_save": "💾 Сохранить", "tut_title": "🚀 Добро пожаловать", "tut_btn": "Начать!"},
    "Chinese Simplified": {"scan": "🔍 扫描系统", "appwiz": "⚙️ 卸载应用", "settings": "🎨 设置", "main_title": "高级追踪", "placeholder": "输入名称并按 ENTER...", "status_ready": "就绪。 (双击打开)", "btn_clean": "✨ 清理安全残留", "col_type": "类型", "col_path": "路径", "col_risk": "风险", "ctx_open": "📂 打开", "ctx_del": "🗑️ 删除", "set_title": "设置", "set_theme": "主题", "set_lang": "语言", "set_save": "💾 保存", "tut_title": "🚀 欢迎", "tut_btn": "开始!"},
    "Chinese Traditional": {"scan": "🔍 掃描系統", "appwiz": "⚙️ 卸載應用", "settings": "🎨 設置", "main_title": "高級追蹤", "placeholder": "輸入名稱並按 ENTER...", "status_ready": "就緒。 (雙擊打開)", "btn_clean": "✨ 清理安全殘留", "col_type": "類型", "col_path": "路徑", "col_risk": "風險", "ctx_open": "📂 打開", "ctx_del": "🗑️ 刪除", "set_title": "設置", "set_theme": "主題", "set_lang": "語言", "set_save": "💾 保存", "tut_title": "🚀 歡迎", "tut_btn": "開始!"},
    "Japanese": {"scan": "🔍 スキャン", "appwiz": "⚙️ アンインストール", "settings": "🎨 設定", "main_title": "高度なトラッカー", "placeholder": "名前を入力してENTER...", "status_ready": "準備完了。 (ダブルクリックで開く)", "btn_clean": "✨ 安全な残骸をクリーン", "col_type": "タイプ", "col_path": "パス", "col_risk": "リスク", "ctx_open": "📂 開く", "ctx_del": "🗑️ 削除", "set_title": "設定", "set_theme": "テーマ", "set_lang": "言語", "set_save": "💾 保存", "tut_title": "🚀 ようこそ", "tut_btn": "開始!"},
    "Korean": {"scan": "🔍 시스템 스캔", "appwiz": "⚙️ 앱 제거", "settings": "🎨 설정", "main_title": "고급 트래커", "placeholder": "이름을 입력하고 ENTER...", "status_ready": "준비. (더블클릭하여 열기)", "btn_clean": "✨ 안전 정리", "col_type": "유형", "col_path": "경로", "col_risk": "위험", "ctx_open": "📂 열기", "ctx_del": "🗑️ 삭제", "set_title": "설정", "set_theme": "테마", "set_lang": "언어", "set_save": "💾 저장", "tut_title": "🚀 환영합니다", "tut_btn": "시작!"},
    "Italian": {"scan": "🔍 Scansiona", "appwiz": "⚙️ Disinstalla", "settings": "🎨 Impostazioni", "main_title": "Tracciatore Avanzato", "placeholder": "Digita un nome e premi INVIO...", "status_ready": "Pronto.", "btn_clean": "✨ Pulisci Sicuri", "col_type": "TIPO", "col_path": "PERCORSO", "col_risk": "RISCHIO", "ctx_open": "📂 Apri", "ctx_del": "🗑️ Elimina", "set_title": "Impostazioni", "set_theme": "Tema", "set_lang": "Lingua", "set_save": "💾 Salva", "tut_title": "🚀 Benvenuto", "tut_btn": "Inizia!"},
    "Portuguese": {"scan": "🔍 Escanear", "appwiz": "⚙️ Desinstalar", "settings": "🎨 Configurações", "main_title": "Rastreador Avançado", "placeholder": "Digite um nome e ENTER...", "status_ready": "Pronto.", "btn_clean": "✨ Limpar Seguros", "col_type": "TIPO", "col_path": "CAMINHO", "col_risk": "RISCO", "ctx_open": "📂 Abrir", "ctx_del": "🗑️ Excluir", "set_title": "Configurações", "set_theme": "Tema", "set_lang": "Idioma", "set_save": "💾 Salvar", "tut_title": "🚀 Bem-vindo", "tut_btn": "Começar!"},
    "Dutch": {"scan": "🔍 Scannen", "appwiz": "⚙️ Verwijderen", "settings": "🎨 Instellingen", "main_title": "Geavanceerde Tracker", "placeholder": "Typ naam en druk op ENTER...", "status_ready": "Klaar.", "btn_clean": "✨ Veilige Wissen", "col_type": "TYPE", "col_path": "PAD", "col_risk": "RISICO", "ctx_open": "📂 Open", "ctx_del": "🗑️ Verwijder", "set_title": "Instellingen", "set_theme": "Thema", "set_lang": "Taal", "set_save": "💾 Opslaan", "tut_title": "🚀 Welkom", "tut_btn": "Starten!"},
    "Polish": {"scan": "🔍 Skanuj", "appwiz": "⚙️ Odinstaluj", "settings": "🎨 Ustawienia", "main_title": "Zaawansowany Śledzik", "placeholder": "Wpisz nazwę i ENTER...", "status_ready": "Gotowe.", "btn_clean": "✨ Wyczyść Bezpieczne", "col_type": "TYP", "col_path": "ŚCIEŻKA", "col_risk": "RYZYKO", "ctx_open": "📂 Otwórz", "ctx_del": "🗑️ Usuń", "set_title": "Ustawienia", "set_theme": "Motyw", "set_lang": "Język", "set_save": "💾 Zapisz", "tut_title": "🚀 Witaj", "tut_btn": "Rozpocznij!"},
    "Czech": {"scan": "🔍 Skenovat", "appwiz": "⚙️ Odinstalovat", "settings": "🎨 Nastavení", "main_title": "Pokročilé Sledování", "placeholder": "Zadejte název...", "status_ready": "Připraveno.", "btn_clean": "✨ Vyčistit", "ctx_open": "📂 Otevřít", "ctx_del": "🗑️ Smazat", "set_title": "Nastavení", "set_save": "💾 Uložit", "tut_title": "🚀 Vítejte", "tut_btn": "Začít!"},
    "Danish": {"scan": "🔍 Scan", "appwiz": "⚙️ Afinstaller", "settings": "🎨 Indstillinger", "main_title": "Avanceret Sporing", "placeholder": "Skriv navn...", "status_ready": "Klar.", "btn_clean": "✨ Rens", "ctx_open": "📂 Åbn", "ctx_del": "🗑️ Slet", "set_title": "Indstillinger", "set_save": "💾 Gem", "tut_title": "🚀 Velkommen", "tut_btn": "Start!"},
    "Filipino": {"scan": "🔍 I-scan", "appwiz": "⚙️ I-uninstall", "settings": "🎨 Mga Setting", "main_title": "Advanced Tracker", "placeholder": "I-type ang pangalan...", "status_ready": "Handa na.", "btn_clean": "✨ Linisin", "ctx_open": "📂 Buksan", "ctx_del": "🗑️ Tanggalin", "set_title": "Mga Setting", "set_save": "💾 I-save", "tut_title": "🚀 Maligayang pagdating", "tut_btn": "Simulan!"},
    "Finnish": {"scan": "🔍 Skannaa", "appwiz": "⚙️ Poista", "settings": "🎨 Asetukset", "main_title": "Kehittynyt Seuranta", "placeholder": "Kirjoita nimi...", "status_ready": "Valmis.", "btn_clean": "✨ Puhdista", "ctx_open": "📂 Avaa", "ctx_del": "🗑️ Poista", "set_title": "Asetukset", "set_save": "💾 Tallenna", "tut_title": "🚀 Tervetuloa", "tut_btn": "Aloita!"},
    "Greek": {"scan": "🔍 Σάρωση", "appwiz": "⚙️ Απεγκατάσταση", "settings": "🎨 Ρυθμίσεις", "main_title": "Προηγμένη Παρακολούθηση", "placeholder": "Πληκτρολογήστε όνομα...", "status_ready": "Έτοιμο.", "btn_clean": "✨ Καθαρισμός", "ctx_open": "📂 Άνοιγμα", "ctx_del": "🗑️ Διαγραφή", "set_title": "Ρυθμίσεις", "set_save": "💾 Αποθήκευση", "tut_title": "🚀 Καλώς ήρθατε", "tut_btn": "Έναρξη!"},
    "Hindi": {"scan": "🔍 स्कैन", "appwiz": "⚙️ अनइंस्टॉल", "settings": "🎨 सेटिंग्स", "main_title": "उन्नत ट्रैकर", "placeholder": "नाम टाइप करें...", "status_ready": "तैयार।", "btn_clean": "✨ साफ करें", "ctx_open": "📂 खोलें", "ctx_del": "🗑️ हटाएं", "set_title": "सेटिंग्स", "set_save": "💾 सहेजें", "tut_title": "🚀 स्वागत है", "tut_btn": "शुरू करें!"},
    "Hungarian": {"scan": "🔍 Vizsgálat", "appwiz": "⚙️ Eltávolítás", "settings": "🎨 Beállítások", "main_title": "Haladó Követő", "placeholder": "Írj be egy nevet...", "status_ready": "Kész.", "btn_clean": "✨ Törlés", "ctx_open": "📂 Megnyitás", "ctx_del": "🗑️ Törlés", "set_title": "Beállítások", "set_save": "💾 Mentés", "tut_title": "🚀 Üdvözlünk", "tut_btn": "Kezdés!"},
    "Indonesian": {"scan": "🔍 Pindai", "appwiz": "⚙️ Copot", "settings": "🎨 Pengaturan", "main_title": "Pelacak Lanjutan", "placeholder": "Ketik nama...", "status_ready": "Siap.", "btn_clean": "✨ Bersihkan", "ctx_open": "📂 Buka", "ctx_del": "🗑️ Hapus", "set_title": "Pengaturan", "set_save": "💾 Simpan", "tut_title": "🚀 Selamat Datang", "tut_btn": "Mulai!"},
    "Malay": {"scan": "🔍 Imbas", "appwiz": "⚙️ Nyahpasang", "settings": "🎨 Tetapan", "main_title": "Penjejak Lanjutan", "placeholder": "Taip nama...", "status_ready": "Sedia.", "btn_clean": "✨ Bersihkan", "ctx_open": "📂 Buka", "ctx_del": "🗑️ Padam", "set_title": "Tetapan", "set_save": "💾 Simpan", "tut_title": "🚀 Selamat Datang", "tut_btn": "Mula!"},
    "Norwegian": {"scan": "🔍 Skann", "appwiz": "⚙️ Avinstaller", "settings": "🎨 Innstillinger", "main_title": "Avansert Sporer", "placeholder": "Skriv navn...", "status_ready": "Klar.", "btn_clean": "✨ Rens", "ctx_open": "📂 Åpne", "ctx_del": "🗑️ Slett", "set_title": "Innstillinger", "set_save": "💾 Lagre", "tut_title": "🚀 Velkommen", "tut_btn": "Start!"},
    "Romanian": {"scan": "🔍 Scanare", "appwiz": "⚙️ Dezinstalare", "settings": "🎨 Setări", "main_title": "Urmărire Avansată", "placeholder": "Tastați un nume...", "status_ready": "Pregătit.", "btn_clean": "✨ Curăță", "ctx_open": "📂 Deschide", "ctx_del": "🗑️ Șterge", "set_title": "Setări", "set_save": "💾 Salvează", "tut_title": "🚀 Bun venit", "tut_btn": "Începe!"},
    "Slovak": {"scan": "🔍 Skenovať", "appwiz": "⚙️ Odinštalovať", "settings": "🎨 Nastavenia", "main_title": "Pokročilé Sledovanie", "placeholder": "Zadajte názov...", "status_ready": "Pripravené.", "btn_clean": "✨ Vyčistiť", "ctx_open": "📂 Otvoriť", "ctx_del": "🗑️ Zmazať", "set_title": "Nastavenia", "set_save": "💾 Uložiť", "tut_title": "🚀 Vitajte", "tut_btn": "Začať!"},
    "Swedish": {"scan": "🔍 Skanna", "appwiz": "⚙️ Avinstallera", "settings": "🎨 Inställningar", "main_title": "Avancerad Spårare", "placeholder": "Skriv namn...", "status_ready": "Redo.", "btn_clean": "✨ Rensa", "ctx_open": "📂 Öppna", "ctx_del": "🗑️ Ta bort", "set_title": "Inställningar", "set_save": "💾 Spara", "tut_title": "🚀 Välkommen", "tut_btn": "Börja!"},
    "Thai": {"scan": "🔍 สแกน", "appwiz": "⚙️ ถอนการติดตั้ง", "settings": "🎨 การตั้งค่า", "main_title": "ตัวติดตามขั้นสูง", "placeholder": "พิมพ์ชื่อ...", "status_ready": "พร้อม.", "btn_clean": "✨ ล้าง", "ctx_open": "📂 เปิด", "ctx_del": "🗑️ ลบ", "set_title": "การตั้งค่า", "set_save": "💾 บันทึก", "tut_title": "🚀 ยินดีต้อนรับ", "tut_btn": "เริ่ม!"},
    "Ukrainian": {"scan": "🔍 Сканувати", "appwiz": "⚙️ Видалити", "settings": "🎨 Налаштування", "main_title": "Розширений Трекер", "placeholder": "Введіть ім'я...", "status_ready": "Готово.", "btn_clean": "✨ Очистити", "ctx_open": "📂 Відкрити", "ctx_del": "🗑️ Видалити", "set_title": "Налаштування", "set_save": "💾 Зберегти", "tut_title": "🚀 Ласкаво просимо", "tut_btn": "Почати!"},
    "Vietnamese": {"scan": "🔍 Quét", "appwiz": "⚙️ Gỡ Cài Đặt", "settings": "🎨 Cài Đặt", "main_title": "Trình Theo Dõi Nâng Cao", "placeholder": "Nhập tên...", "status_ready": "Sẵn sàng.", "btn_clean": "✨ Dọn Dẹp", "ctx_open": "📂 Mở", "ctx_del": "🗑️ Xóa", "set_title": "Cài Đặt", "set_save": "💾 Lưu", "tut_title": "🚀 Chào mừng", "tut_btn": "Bắt Đầu!"}
}

# ==========================================
# OTOMATİK SİSTEM DİLİ ALGILAMA (29 DİL)
# ==========================================
def detect_system_language():
    try:
        lang_code, _ = locale.getdefaultlocale()
        if lang_code:
            l = lang_code.lower()
            if l.startswith('tr'): return "Turkish"
            if l.startswith('cs'): return "Czech"
            if l.startswith('da'): return "Danish"
            if l.startswith('nl'): return "Dutch"
            if l.startswith('fil'): return "Filipino"
            if l.startswith('fi'): return "Finnish"
            if l.startswith('fr'): return "French"
            if l.startswith('de'): return "German"
            if l.startswith('el'): return "Greek"
            if l.startswith('hi'): return "Hindi"
            if l.startswith('hu'): return "Hungarian"
            if l.startswith('id'): return "Indonesian"
            if l.startswith('it'): return "Italian"
            if l.startswith('ja'): return "Japanese"
            if l.startswith('ko'): return "Korean"
            if l.startswith('ms'): return "Malay"
            if l.startswith('no'): return "Norwegian"
            if l.startswith('pl'): return "Polish"
            if l.startswith('pt'): return "Portuguese"
            if l.startswith('ro'): return "Romanian"
            if l.startswith('sk'): return "Slovak"
            if l.startswith('es'): return "Spanish"
            if l.startswith('sv'): return "Swedish"
            if l.startswith('th'): return "Thai"
            if l.startswith('uk'): return "Ukrainian"
            if l.startswith('vi'): return "Vietnamese"
            if l.startswith('ru'): return "Russian"
            if l == 'zh_tw' or l == 'zh_hk': return "Chinese Traditional"
            if l.startswith('zh'): return "Chinese Simplified"
    except: pass
    return "English"

# ==========================================
# GÖRSEL STİL VE KONTROL
# ==========================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def is_admin():
    try: return ctypes.windll.shell32.IsUserAnAdmin()
    except: return False

class HyperZeroApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.current_lang = detect_system_language() 
        if self.current_lang not in LANGUAGES:
            self.current_lang = "English"

        self.withdraw() 
        self.title("HyperZero v1.0 - Global Edition")
        self.geometry("1000x700")
        self.show_splash_screen()

    # GÜVENLİ ÇEVİRİ FONKSİYONU (CRASH ÖNLEYİCİ)
    def t(self, key):
        """Eğer seçili dilde kelime yoksa otomatik olarak İngilizce'den çeker, program çökmez."""
        lang_dict = LANGUAGES.get(self.current_lang, LANGUAGES["English"])
        return lang_dict.get(key, LANGUAGES["English"].get(key, ""))

    def show_splash_screen(self):
        self.splash = ctk.CTkToplevel(self)
        self.splash.overrideredirect(True)
        
        window_width, window_height = 400, 300
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.splash.geometry(f"{window_width}x{window_height}+{x}+{y}")

        splash_frame = ctk.CTkFrame(self.splash, corner_radius=20, fg_color=("#F9F9FA", "#1A1A1A"), border_width=2, border_color="#3B8ED0")
        splash_frame.pack(fill="both", expand=True)

        ctk.CTkLabel(splash_frame, text="⚡", font=ctk.CTkFont(size=70), text_color=("#101010", "white")).pack(pady=(60, 10))
        ctk.CTkLabel(splash_frame, text="HYPERZERO", font=ctk.CTkFont(size=28, weight="bold"), text_color=("#101010", "white")).pack()
        ctk.CTkLabel(splash_frame, text="Loading Global Interface...", font=ctk.CTkFont(size=12), text_color="#3B8ED0").pack(pady=20)

        Timer(1.0, self.init_main_window).start()

    def init_main_window(self):
        self.splash.destroy()
        self.deiconify() 

        # SOL MENÜ
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=("#F0F0F0", "#1A1A1A"))
        self.sidebar.pack(side="left", fill="y")

        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(pady=40, padx=20)
        ctk.CTkLabel(logo_frame, text="⚡", font=ctk.CTkFont(size=26), text_color=("#101010", "white")).pack(side="left") 
        ctk.CTkLabel(logo_frame, text="HYPERZERO", font=ctk.CTkFont(size=20, weight="bold"), text_color=("#101010", "white")).pack(side="left")

        self.btn_scan = ctk.CTkButton(self.sidebar, text="", command=self.start_scan_thread,
                                     font=ctk.CTkFont(size=13, weight="bold"), height=42, corner_radius=8, 
                                     fg_color=("#E5E5E8", "#2B2B2B"), text_color=("#101010", "white"), hover_color="#3B8ED0", anchor="w") 
        self.btn_scan.pack(pady=8, padx=15, fill="x")

        self.btn_appwiz = ctk.CTkButton(self.sidebar, text="", command=self.open_control_panel,
                                     font=ctk.CTkFont(size=13), height=42, corner_radius=8, 
                                     fg_color="transparent", border_width=1, border_color="#3B8ED0", 
                                     text_color=("#101010", "white"), hover_color=("#E5E5E8", "#2B2B2B"), anchor="w") 
        self.btn_appwiz.pack(pady=8, padx=15, fill="x")

        self.btn_settings = ctk.CTkButton(self.sidebar, text="", command=self.open_settings,
                                     font=ctk.CTkFont(size=13), height=42, corner_radius=8, 
                                     fg_color="transparent", border_width=1, border_color="#3B8ED0", 
                                     text_color=("#101010", "white"), hover_color=("#E5E5E8", "#2B2B2B"), anchor="w") 
        self.btn_settings.pack(pady=8, padx=15, fill="x")

        self.admin_color = "#2ECC71" if is_admin() else "#E74C3C"
        self.lbl_admin = ctk.CTkLabel(self.sidebar, text="", font=ctk.CTkFont(size=10, weight="bold"), text_color=self.admin_color)
        self.lbl_admin.pack(side="bottom", pady=(0, 20))
        
        self.lbl_version = ctk.CTkLabel(self.sidebar, text="", font=ctk.CTkFont(size=10), text_color="gray")
        self.lbl_version.pack(side="bottom", pady=(20, 5))

        # ANA PANEL
        self.main_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="transparent")
        self.main_frame.pack(side="right", fill="both", expand=True, padx=25, pady=25)

        search_card = ctk.CTkFrame(self.main_frame, corner_radius=12, fg_color=("#FFFFFF", "#1A1A1A"), border_width=1, border_color=("#E5E5E8", "#2B2B2B"))
        search_card.pack(fill="x", pady=(0, 15))

        self.lbl_main_title = ctk.CTkLabel(search_card, text="", font=ctk.CTkFont(size=16, weight="bold"), text_color="#3B8ED0")
        self.lbl_main_title.pack(pady=(15, 5), padx=20, anchor="w")

        self.search_entry = ctk.CTkEntry(search_card, placeholder_text="", height=45, 
                                         corner_radius=8, border_color=("#CCCCCC", "#333333"), fg_color=("#F9F9FA", "#252525"), text_color=("#101010", "white"))
        self.search_entry.pack(pady=(5, 15), padx=20, fill="x")
        self.search_entry.bind("<Return>", lambda event: self.start_scan_thread())

        table_frame = ctk.CTkFrame(self.main_frame, corner_radius=12, fg_color=("#FFFFFF", "#1A1A1A"))
        table_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        tree_scroll = ctk.CTkScrollbar(table_frame)
        tree_scroll.pack(side="right", fill="y", pady=5, padx=5)

        self.tree = ttk.Treeview(table_frame, columns=("Tip", "Yol", "Risk"), show="headings", yscrollcommand=tree_scroll.set)
        self.tree.pack(side="left", fill="both", expand=True, pady=5, padx=5)
        tree_scroll.configure(command=self.tree.yview)

        self.tree.column("Tip", width=130, anchor="center")
        self.tree.column("Yol", width=540, anchor="w")
        self.tree.column("Risk", width=120, anchor="center")

        self.tree.tag_configure("safe", foreground="#2ECC71")
        self.tree.tag_configure("risky", foreground="#E74C3C")

        self.tree.bind("<Button-3>", self.show_context_menu)
        self.tree.bind("<Double-1>", self.open_file_location) 
        
        self.context_menu = tk.Menu(self, tearoff=0, font=("Inter", 10))
        self.context_menu.add_command(label="", command=self.open_selected_location)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="", command=self.delete_selected_item)

        bottom_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        bottom_frame.pack(fill="x")
        self.lbl_status = ctk.CTkLabel(bottom_frame, text="", text_color="gray")
        self.lbl_status.pack(side="left")
        self.btn_auto_clean = ctk.CTkButton(bottom_frame, text="", command=self.auto_delete_safe_items,
                                           fg_color="#C0392B", hover_color="#A93226")
        self.btn_auto_clean.pack(side="right")

        self.apply_language(self.current_lang)
        self.apply_theme_style(ctk.get_appearance_mode())
        self.after(500, self.show_welcome_tutorial)

    # ==========================================
    # GÜVENLİ DİL (İ18N) UYGULAMASI
    # ==========================================
    def apply_language(self, lang_name):
        self.current_lang = lang_name

        self.btn_scan.configure(text=self.t("scan"))
        self.btn_appwiz.configure(text=self.t("appwiz"))
        self.btn_settings.configure(text=self.t("settings"))
        self.lbl_main_title.configure(text=self.t("main_title"))
        self.search_entry.configure(placeholder_text=self.t("placeholder"))
        self.lbl_status.configure(text=self.t("status_ready"))
        self.btn_auto_clean.configure(text=self.t("btn_clean"))
        self.lbl_version.configure(text=self.t("ver"))
        self.lbl_admin.configure(text=self.t("admin") if is_admin() else self.t("no_admin"))

        self.tree.heading("Tip", text=self.t("col_type"))
        self.tree.heading("Yol", text=self.t("col_path"))
        self.tree.heading("Risk", text=self.t("col_risk"))

        self.context_menu.entryconfig(0, label=self.t("ctx_open"))
        self.context_menu.entryconfig(2, label=self.t("ctx_del"))

    # ==========================================
    # TEMA VE AYARLAR YÖNETİMİ
    # ==========================================
    def apply_theme_style(self, mode_name):
        style = ttk.Style()
        style.theme_use("default") 
        if mode_name.lower() == "dark":
            style.configure("Treeview", background="#1A1A1A", foreground="#E0E0E0", fieldbackground="#1A1A1A", borderwidth=0, rowheight=32)
            style.map('Treeview', background=[('selected', '#3B8ED0')])
            style.configure("Treeview.Heading", background="#252525", foreground="white", font=('Inter', 11, 'bold'))
            self.context_menu.config(bg="#252525", fg="white", activebackground="#3B8ED0")
        else:
            style.configure("Treeview", background="#FFFFFF", foreground="#101010", fieldbackground="#FFFFFF", borderwidth=0, rowheight=32)
            style.map('Treeview', background=[('selected', '#3B8ED0')])
            style.configure("Treeview.Heading", background="#E5E5E8", foreground="black", font=('Inter', 11, 'bold'))
            self.context_menu.config(bg="#FFFFFF", fg="black", activebackground="#3B8ED0")

    def open_settings(self):
        if hasattr(self, "settings_win") and self.settings_win is not None and self.settings_win.winfo_exists():
            self.settings_win.focus()
            return

        self.settings_win = ctk.CTkToplevel(self)
        self.settings_win.title(self.t("set_title"))
        self.settings_win.geometry("380x300")
        self.settings_win.attributes('-topmost', True) 

        x = self.winfo_x() + (self.winfo_width() // 2) - 190
        y = self.winfo_y() + (self.winfo_height() // 2) - 150
        self.settings_win.geometry(f"+{x}+{y}")

        ctk.CTkLabel(self.settings_win, text=self.t("set_theme"), font=ctk.CTkFont(size=14, weight="bold"), text_color=("#101010", "white")).pack(pady=(15, 5))
        theme_var = ctk.StringVar(value=ctk.get_appearance_mode().capitalize())
        ctk.CTkSegmentedButton(self.settings_win, values=["Light", "Dark"], variable=theme_var).pack(pady=5)

        ctk.CTkLabel(self.settings_win, text=self.t("set_lang"), font=ctk.CTkFont(size=14, weight="bold"), text_color=("#101010", "white")).pack(pady=(15, 5))
        lang_var = ctk.StringVar(value=self.current_lang)
        # TAM 29 DİL LİSTESİ
        lang_list = sorted(list(LANGUAGES.keys()))
        lang_menu = ctk.CTkOptionMenu(self.settings_win, values=lang_list, variable=lang_var)
        lang_menu.pack(pady=5)

        def save_and_apply():
            ctk.set_appearance_mode(theme_var.get())
            self.apply_theme_style(theme_var.get())
            self.apply_language(lang_var.get())
            self.settings_win.destroy()

        ctk.CTkButton(self.settings_win, text=self.t("set_save"), command=save_and_apply, font=ctk.CTkFont(weight="bold"), 
                      fg_color="#2ECC71", hover_color="#27AE60", text_color="white", height=40).pack(pady=(25, 10))

    # ==========================================
    # REHBER / GÜNCELLEME NOTLARI
    # ==========================================
    def show_welcome_tutorial(self):
        self.tutorial_window = ctk.CTkToplevel(self)
        self.tutorial_window.title(self.t("tut_title"))
        
        self.tutorial_window.geometry("700x650")
        self.tutorial_window.transient(self)
        self.tutorial_window.grab_set()

        x = self.winfo_x() + (self.winfo_width() // 2) - 350
        y = self.winfo_y() + (self.winfo_height() // 2) - 325
        self.tutorial_window.geometry(f"+{x}+{y}")

        title_lbl = ctk.CTkLabel(self.tutorial_window, text=self.t("tut_title"), font=ctk.CTkFont(size=22, weight="bold"), text_color="#3B8ED0")
        title_lbl.pack(pady=(25, 10))

        info_box = ctk.CTkTextbox(self.tutorial_window, font=("Inter", 14), wrap="word", 
                                  fg_color=("#F9F9FA", "#1A1A1A"), border_width=1, border_color=("#E5E5E8", "#2B2B2B"), text_color=("#101010", "white"))
        info_box.pack(fill="both", expand=True, padx=25, pady=10)

        info_box.insert("0.0", self.t("tut_body"))
        info_box.configure(state="disabled")

        btn_start = ctk.CTkButton(self.tutorial_window, text=self.t("tut_btn"), command=self.tutorial_window.destroy, 
                                  font=ctk.CTkFont(size=14, weight="bold"), height=45, fg_color="#3B8ED0", hover_color="#2980B9", text_color="white")
        btn_start.pack(pady=(15, 25))

    # ==========================================
    # NAVİGASYON VE UYGULAMA KALDIR
    # ==========================================
    def open_control_panel(self):
        try: subprocess.Popen("control appwiz.cpl")
        except Exception: pass

    def open_file_location(self, event):
        self.open_selected_location()

    def open_selected_location(self):
        sel = self.tree.selection()
        if not sel: return
        item_values = self.tree.item(sel[0], 'values')
        item_type, path = item_values[0], item_values[1]

        try:
            if "REGISTRY" in item_type.upper() or "Kayıt" in item_type or item_type.startswith("⚙️"):
                reg_path = path
                if path.startswith("HKCU"): reg_path = path.replace("HKCU", "HKEY_CURRENT_USER")
                elif path.startswith("HKLM"): reg_path = path.replace("HKLM", "HKEY_LOCAL_MACHINE")

                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Applets\Regedit", 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(key, "LastKey", 0, winreg.REG_SZ, f"Computer\\{reg_path}")
                winreg.CloseKey(key)
                subprocess.Popen("regedit.exe")
            else:
                if not os.path.exists(path): return
                if os.path.isfile(path): subprocess.Popen(f'explorer /select,"{path}"')
                else: subprocess.Popen(f'explorer "{path}"')
        except Exception: pass

    # ==========================================
    # GELİŞMİŞ MOTOR FONKSİYONLARI
    # ==========================================
    def assess_risk(self, path):
        risk_keywords = ['windows', 'system32', 'microsoft', 'drivers', 'boot', 'recovery']
        if any(kw in path.lower() for kw in risk_keywords): return "Kritik"
        return "Güvenli"

    def _add_to_tree(self, item_type, path, risk, tag):
        self.tree.insert("", "end", values=(item_type, path, risk), tags=(tag,))

    def start_scan_thread(self):
        query = self.search_entry.get().strip()
        if len(query) < 3: return
        self.btn_scan.configure(state="disabled")
        for item in self.tree.get_children(): self.tree.delete(item)
        threading.Thread(target=self.perform_deep_scan, args=(query,), daemon=True).start()

    def perform_deep_scan(self, query):
        q = query.lower()
        user_profile = os.environ.get('USERPROFILE', '')
        onedrive = os.environ.get('ONEDRIVE', '')
        
        target_dirs = {
            "Masaüstü": os.path.join(user_profile, 'Desktop') if user_profile else None,
            "OneDrive": os.path.join(onedrive, 'Desktop') if onedrive else None,
            "Belgeler": os.path.join(user_profile, 'Documents') if user_profile else None,
            "AppData": os.environ.get('APPDATA'),
            "LocalApp": os.environ.get('LOCALAPPDATA'),
            "ProgramData": os.environ.get('PROGRAMDATA', 'C:\\ProgramData'),
        }

        drives = [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]
        for drive in drives:
            target_dirs[f"PrgFiles ({drive[0]})"] = os.path.join(drive, "Program Files")
            target_dirs[f"PrgFiles x86 ({drive[0]})"] = os.path.join(drive, "Program Files (x86)")
            target_dirs[f"Steam ({drive[0]})"] = os.path.join(drive, "Program Files (x86)", "Steam", "steamapps", "common")
            target_dirs[f"SteamLib ({drive[0]})"] = os.path.join(drive, "SteamLibrary", "steamapps", "common")
            target_dirs[f"Epic ({drive[0]})"] = os.path.join(drive, "Program Files", "Epic Games")

        for tip, base_path in target_dirs.items():
            if base_path and os.path.exists(base_path):
                try:
                    for root, dirs, files in os.walk(base_path):
                        for d in dirs:
                            if q in d.lower():
                                full_p = os.path.join(root, d)
                                risk = self.assess_risk(full_p)
                                tag = "risky" if risk == "Kritik" else "safe"
                                self.after(0, self._add_to_tree, f"📁 {tip}", full_p, risk, tag)
                        for f in files:
                            if q in f.lower():
                                full_p = os.path.join(root, f)
                                risk = self.assess_risk(full_p)
                                tag = "risky" if risk == "Kritik" else "safe"
                                self.after(0, self._add_to_tree, f"📄 File", full_p, risk, tag)
                        if root.count(os.sep) - base_path.count(os.sep) >= 3: del dirs[:]
                except: pass

        reg_hives = [
            (winreg.HKEY_CURRENT_USER, r"Software", "HKCU"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software", "HKLM"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", "Uninstall"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall", "Uninstall (x86)")
        ]

        for hive, base_path, hive_name in reg_hives:
            try:
                with winreg.OpenKey(hive, base_path) as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        try:
                            sub_name = winreg.EnumKey(key, i)
                            if q in sub_name.lower():
                                full_reg = f"{hive_name}\\{base_path}\\{sub_name}"
                                self.after(0, self._add_to_tree, "⚙️ Registry", full_reg, "Güvenli", "safe")
                        except: pass
            except: pass

        self.after(0, lambda: self.btn_scan.configure(state="normal"))

    # ==========================================
    # GERÇEK SİLME MANTIĞI
    # ==========================================
    def execute_physical_deletion(self, item_type, path):
        try:
            if "REGISTRY" in item_type.upper() or "Kayıt" in item_type or item_type.startswith("⚙️"):
                real_path = path.replace("Uninstall\\", "").replace("Uninstall (x86)\\", "")
                cmd = f'reg delete "{real_path}" /f'
                CREATE_NO_WINDOW = 0x08000000 
                result = subprocess.run(cmd, shell=True, capture_output=True, creationflags=CREATE_NO_WINDOW)
                if result.returncode != 0: return False, "Erişim Engellendi (Yönetici İzni)"
                return True, "Başarılı"
            
            if not os.path.exists(path): return True, "Zaten silinmiş."
            try: os.chmod(path, stat.S_IWRITE) 
            except: pass

            try:
                if os.path.isfile(path): os.remove(path)
                elif os.path.isdir(path):
                    def remove_readonly(func, p, _):
                        os.chmod(p, stat.S_IWRITE)
                        func(p)
                    shutil.rmtree(path, onerror=remove_readonly)
            except: pass
            
            if os.path.exists(path):
                CREATE_NO_WINDOW = 0x08000000 
                if os.path.isfile(path): subprocess.run(f'del /f /q /a "{path}"', shell=True, creationflags=CREATE_NO_WINDOW)
                else: subprocess.run(f'rmdir /s /q "{path}"', shell=True, creationflags=CREATE_NO_WINDOW)

            if os.path.exists(path): return False, "Dosya şu an kullanımda."
            return True, "Başarılı"
        except Exception as e: return False, str(e)

    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def delete_selected_item(self):
        sel = self.tree.selection()
        if not sel: return
        item_values = self.tree.item(sel[0], 'values')
        
        if "Kritik" in item_values[2] or "Critical" in item_values[2] or "Критич" in item_values[2] or "RISIKO" in item_values[2] or "RIESGO" in item_values[2] or "RISQUE" in item_values[2]:
            confirm = messagebox.askyesno("Uyarı", f"DİKKAT: Windows zarar görebilir!\nYol: {item_values[1]}\nSilinsin mi?", icon='warning')
        else:
            confirm = messagebox.askyesno("Kesin Sil", f"Tamamen yok edilecek:\n{item_values[1]}\nOnaylıyor musunuz?")

        if confirm:
            success, msg = self.execute_physical_deletion(item_values[0], item_values[1])
            if success: self.tree.delete(sel[0])
            else: messagebox.showerror("Hata", msg)

    def auto_delete_safe_items(self):
        confirm = messagebox.askyesno("Toplu Temizlik", "Tüm 'Güvenli' ögeler silinecek. Devam edilsin mi?")
        if not confirm: return 
        for child in reversed(self.tree.get_children()):
            val = self.tree.item(child, 'values')[2]
            if "Güvenli" in val or "Safe" in val or "Безопас" in val or "Sichere" in val or "Seguros" in val or "Sûrs" in val:
                succ, _ = self.execute_physical_deletion(self.tree.item(child, 'values')[0], self.tree.item(child, 'values')[1])
                if succ: self.tree.delete(child)

if __name__ == "__main__":
    app = HyperZeroApp()
    app.mainloop()