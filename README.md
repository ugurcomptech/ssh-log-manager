
# Merkezî SSH Log Yönetim Sistemi (Agent-Client)

Bu proje, SSH loglarını merkezi bir sistemde toplayan bir Agent-Client yapısını içerir. SSH giriş ve çıkış başarıları, başarısız denemeler merkezi sunucuya gönderilir ve lokal olarak depolanır. Flask tabanlı merkezi sunucu, verileri alır ve günlük dosyasını oluşturur. Her bir agent, yerel logları takip eder ve başarı/başarısız giriş bilgilerini merkeze iletir.

## Proje Bileşenleri

1. **Merkezi Sunucu (Flask)**: SSH loglarını alır, işler ve günlükleri kaydeder.
2. **Agent**: Yerel SSH loglarını okur, işlem yapar ve verileri merkezi sunucuya gönderir.

## Kurulum ve Kullanım

### 1. Gereksinimler

Aşağıdaki bağımlılıkları yüklemek için `requirements.txt` dosyasını kullanabilirsiniz:

```bash
pip install -r requirements.txt
```

### 2. Merkezi Sunucu (Server) Kurulumu

- Flask uygulamasını çalıştırmak için, aşağıdaki komutla sunucuyu başlatın:

```bash
python3 server.py
```

- Bu sunucu, yerel SSH giriş/çıkış loglarını alır ve `log` yoluna gönderir.

### 3. Agent Kurulumu

- Agent, SSH loglarını sürekli takip eder ve başarılı/başarısız girişleri merkezi sunucuya gönderir.
- Agent'ı çalıştırmak için:

```bash
python3 agent.py
```

### 4. Güvenlik

- Yalnızca belirli IP'lerden gelen bağlantılara izin verilir.
- Merkezî sunucu 5000 portu üzerinden JSON verisi alır.

## Kullanım Senaryoları

- SSH girişleri ve başarısız girişler takip edilir.
- Her bir başarılı/başarısız giriş, merkezi sunucuya iletilir.
- Günlük dosyaları, tarih bazında depolanır ve analiz edilmek üzere arşivlenir.

## Katkıda Bulunma

Projenize katkı sağlamak isterseniz, pull request göndererek katkıda bulunabilirsiniz.
