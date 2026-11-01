import json
import os

TODO_FILE = "todo.json"

def load_todos():
    """Görevleri JSON dosyasından yükle"""
    if not os.path.exists(TODO_FILE):
        return []
    try:
        with open(TODO_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('tasks', [])
    except (json.JSONDecodeError, IOError):
        return []

def save_todos(tasks):
    """Görevleri JSON dosyasına kaydet"""
    data = {'tasks': tasks}
    with open(TODO_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_task():
    """Yeni görev ekle"""
    task = input("Görev adı girin: ")
    if not task.strip():
        print("Görev boş olamaz!")
        return
    
    priority = input("Öncelik (1:Düşük, 2:Orta, 3:Yüksek) - Varsayılan: 2: ")
    try:
        priority_level = 3 if priority.strip() == '3' else (2 if priority.strip() == '2' else 1)
    except:
        priority_level = 2
    
    due_date = input("Son tarih (GG/AA) - İsteğe bağlı: ")
    
    task_id = len(load_todos()) + 1
    
    todo = {
        "id": task_id,
        "task": task.strip(),
        "priority": priority_level,
        "due_date": due_date if due_date else "",
        "completed": False
    }
    
    tasks = load_todos()
    tasks.append(todo)
    save_todos(tasks)
    
    print(f"\n✓ Görev eklendi: #{task_id} - {task.strip()}")

def list_tasks():
    """Tüm görevleri listele"""
    tasks = load_todos()
    
    if not tasks:
        print("\nHenüz hiç görev yok!")
        return
    
    print("\n" + "="*60)
    print(f"{'ID':<5} {'GÖREV':<40} {'ÖNCELİK':<10} {'TARİH':<10} {'DURUM':<10}")
    print("="*60)
    
    for task in tasks:
        status = "✓ TAMAMLANDI" if task['completed'] else "⚪ BEKLEMEDE"
        priority_symbol = {"1": "🔹 Düşük", "2": "🟡 Orta", "3": "🔴 Yüksek"}
        
        print(f"{task['id']:<5} {task['task'][:40]:<40} "
              f"{priority_symbol.get(str(task['priority']), '???'):<10} "
              f"{task['due_date'] or '-':<10} {status:<10}")
    
    print("="*60)
    print(f"Toplam görev: {len(tasks)}")

def delete_task():
    """Görev sil"""
    tasks = load_todos()
    
    if not tasks:
        print("\nHenüz hiç görev yok!")
        return
    
    list_tasks()
    
    try:
        task_id = int(input("\nSilmek istediğiniz görevin ID'sini girin: "))
    except ValueError:
        print("Geçersiz ID! Lütfen sayısal bir değer girin.")
        return
    
    deleted_task = None
    new_tasks = []
    
    for task in tasks:
        if task['id'] == task_id:
            deleted_task = task['task']
        else:
            new_tasks.append(task)
    
    if deleted_task:
        tasks = new_tasks
        save_todos(tasks)
        print(f"\n✓ Görev silindi: #{task_id} - {deleted_task}")
    else:
        print(f"\n✗ ID #{task_id}'ye sahip görev bulunamadı!")

def mark_completed():
    """Görevi tamamla"""
    tasks = load_todos()
    
    if not tasks:
        print("\nHenüz hiç görev yok!")
        return
    
    list_tasks()
    
    try:
        task_id = int(input("\nTamamlandı işaretlemek istediğiniz görevin ID'sini girin: "))
    except ValueError:
        print("Geçersiz ID! Lütfen sayısal bir değer girin.")
        return
    
    updated_task = None
    new_tasks = []
    
    for task in tasks:
        if task['id'] == task_id:
            if not task['completed']:
                task['completed'] = True
                updated_task = task['task']
            else:
                print(f"{task['task']} zaten tamamlandı!")
                return
        else:
            new_tasks.append(task)
    
    if updated_task:
        save_todos(new_tasks)
        print(f"\n✓ Görev tamamlandı: #{task_id} - {updated_task}")

def show_help():
    """Yardım mesajı"""
    print("""
TODO YAPILACAKLAR LİSTESİ HEMEN ŞİMDİ KULLANMA REHBERİ:

  1. Görev EKLE [e]
     - Görev adı, öncelik ve son tarih girerek yeni görev ekleyin.
  
  2. Görevleri LİSTELE [l]
     - Tüm görevleri önceleğe göre listelemek için kullanın.
  
  3. Görevi TAMAMLA [c]
     - Tamamlanan görevleri işaretleme.
  
  4. Görev SİL [d]
     - Bitmiş veya iptal edilen görevleri silin.
  
  5. ÇIKIŞ [q]
     - Programdan çıkmak için kullanın (JSON dosyası korunur).

ÖNCELİKLER: 🔹 Düşük - 🟡 Orta - 🔴 Yüksek
""")

def main():
    print("\n" + "="*60)
    print("       WELCOME TO TODO LIST PROGRAM!  ".center(60))
    print("="*60)
    
    while True:
        print("""
        ------------------------------------------------------------------------
        [e] Yeni Görev Ekle | [l] Tüm Görevleri Listele | [c] Görevi Tamamla
        [d] Görev Sil | [h] Yardım | [q] Çıkış
        
        Lütfen bir seçenek seçin: 
        ------------------------------------------------------------------------
        """)
        
        choice = input("Seçenek girin (e/l/c/d/h/q): ").strip().lower()
        
        if choice == 'e':
            add_task()
        elif choice == 'l':
            list_tasks()
        elif choice == 'c':
            mark_completed()
        elif choice == 'd':
            delete_task()
        elif choice == 'h':
            show_help()
        elif choice == 'q':
            response = input("\nÇıkmak istediğinizden emin misiniz? (e/h): ").strip().lower()
            if response in ['e', 'yes', 'y']:
                print("\n👋 Görüşürüz! Dosyanız başarıyla kaydedildi.")
                break
            else:
                print("İşlemden vazgeçtiniz.")
        else:
            print("Geçersiz seçenek! Lütfen 'e/l/c/d/h/q' girin.")

if __name__ == "__main__":
    main()