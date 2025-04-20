
# Merkezi SSH Log Sistemi

Bu proje, SSH bağlantı günlüklerini merkezi bir sunucuda toplamak amacıyla tasarlanmıştır. Hem **merkezi** hem de **agent** bileşenlerinden oluşan bir yapı ile, SSH bağlantı bilgileri merkezi sunucuya gönderilir.

## Bileşenler
- **Merkezi Sunucu (Log Server):** SSH bağlantı bilgilerini alır, logları kaydeder ve günlükleri sıkıştırarak arşivler.
- **Agent:** SSH giriş/çıkış bilgilerini izler ve merkezi sunucuya gönderir.

## Gereksinimler

Bu proje için gerekli Python kütüphaneleri `requirements.txt` dosyasına dahil edilmiştir. Gerekli kütüphaneleri yüklemek için aşağıdaki komutu çalıştırabilirsiniz:

```
pip install -r requirements.txt
```

## Kurulum

### 1. Merkezi Sunucu

Merkezi sunucuyu başlatmak için, aşağıdaki adımları takip edin:

1. **Flask Sunucusunu Başlatın**

   Flask tabanlı sunucu, SSH bağlantı günlüklerini alıp işlemektedir.

   `merkezi.py` dosyasını çalıştırarak sunucuyu başlatabilirsiniz.

   ```bash
   python3 merkezi.py
   ```

2. **Sistemi Servis Olarak Çalıştırmak**


   Sistemi bir servis olarak çalıştırmak için `systemd` kullanabilirsiniz. Aşağıdaki adımları izleyin:
   

   - `/etc/systemd/system/ssh-log-server.service` dosyasını oluşturun:

   ```bash
   sudo nano /etc/systemd/system/ssh-log-server.service
   ```

   - Aşağıdaki içeriği yapıştırın:

   ```ini
   [Unit]
   Description=SSH Log Server
   After=network.target

   [Service]
   ExecStart=/usr/bin/python3 /path/to/merkezi.py
   WorkingDirectory=/path/to/your/project
   User=your_user
   Group=your_group
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   - Servisi etkinleştirin ve başlatın:

   ```bash
   sudo systemctl enable ssh-log-server.service
   sudo systemctl start ssh-log-server.service
   ```

4. **Sunucu Durumunu Kontrol Etme**

   Sunucunun durumunu kontrol etmek için aşağıdaki komutu kullanabilirsiniz:

   ```bash
   sudo systemctl status ssh-log-server.service
   ```

### 2. Agent

Agent, SSH bağlantılarını izler ve merkezi sunucuya gönderir. Agent'ı çalıştırmak için `agent.py` dosyasını kullanabilirsiniz.

1. **Agent'ı Çalıştırın**

   ```bash
   python3 agent.py
   ```

2. **Agent'ı Servis Olarak Çalıştırmak**

   `agent.py` dosyasını bir sistem servisi olarak çalıştırmak için aşağıdaki adımları izleyin:

   - `/etc/systemd/system/ssh-log-agent.service` dosyasını oluşturun:

   ```bash
   sudo nano /etc/systemd/system/ssh-log-agent.service
   ```

   - Aşağıdaki içeriği yapıştırın:

   ```ini
   [Unit]
   Description=SSH Log Agent
   After=network.target

   [Service]
   ExecStart=/usr/bin/python3 /path/to/agent.py
   WorkingDirectory=/path/to/your/project
   User=your_user
   Group=your_group
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   - Servisi etkinleştirin ve başlatın:

   ```bash
   sudo systemctl enable ssh-log-agent.service
   sudo systemctl start ssh-log-agent.service
   ```

3. **Agent Durumunu Kontrol Etme**

   Agent servisini kontrol etmek için:

   ```bash
   sudo systemctl status ssh-log-agent.service
   ```

## Yapı

### Merkezi Sunucu (Log Server)

- `merkezi.py`: Merkezi sunucuda çalışacak olan Flask uygulaması.
- `log_roller.py`: Log dosyalarını işleyip kaydeden script.

### Agent

- `agent.py`: SSH giriş/çıkış bağlantılarını izleyen ve merkezi sunucuya gönderen script.

## Loglar

- Merkezi sunucuda, günlükler `/var/log/ssh_<date>.log` dosyasına kaydedilir.
- Eski loglar, belirli bir süre sonra sıkıştırılıp arşivlenir.

---

Bu proje, SSH giriş/çıkışları hakkında detaylı raporlama yaparak, güvenlik izleme ve analiz süreçlerinizi iyileştirmenize yardımcı olabilir.
