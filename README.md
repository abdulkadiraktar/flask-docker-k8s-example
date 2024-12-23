
# BC4M Project

Bu proje, basit bir Flask API uygulamasını Docker ve Kubernetes üzerinde çalıştırmayı amaçlamaktadır.  
Uygulamada 3 temel endpoint bulunur:

1. **GET /**  
   Dönen JSON: `{"msg":"BC4M"}`

2. **GET /health**  
   Dönen JSON: `{"health":"ok"}`  
   Kubernetes’te livenessProbe olarak kullanıldığında, uygulama sağlığını izler.

3. **POST /**  
   Gönderilen body içeriğini (JSON) olduğu gibi geri döndürür.

## İçindekiler

1. [Ön Gereksinimler](#ön-gereksinimler)  
2. [Proje Dosyaları](#proje-dosyaları)  
3. [Lokal Geliştirme ve Test](#lokal-geliştirme-ve-test)  
4. [Docker Kullanımı](#docker-kullanımı)  
   - [Docker Build ve Run (Manuel)](#docker-build-ve-run-manuel)  
   - [Docker Hub’dan Çekme](#docker-hubdan-çekme)  
5. [Kubernetes Üzerinde Çalıştırma](#kubernetes-üzerinde-çalıştırma)  
   - [Minikube Kurulumu ve Başlatma](#minikube-kurulumu-ve-başlatma)  
   - [Deployment ve Service Uygulama](#deployment-ve-service-uygulama)  
   - [NodePort İle Erişim](#nodeport-ile-erişim)  
6. [Endpoints Testi](#endpoints-testi)  
7. [Son Kontroller](#son-kontroller)

---

## Ön Gereksinimler

- **Python 3.x**  
- **Docker** (Kurulum doğrulama: `docker --version`)  
- **Minikube** veya başka bir Kubernetes ortamı  
- **kubectl** komutu (Kubernetes CLI)

---

## Proje Dosyaları

Proje kök dizininde şu dosyalar bulunur:

- **app.py**: Flask uygulaması  
- **requirements.txt**: Python bağımlılıkları  
- **Dockerfile**: Docker imaj oluşturma dosyası  
- **deployment.yaml**: Kubernetes Deployment manifesti  
- **service.yaml**: Kubernetes Service manifesti  
- **README.md**: Bu doküman  

---

## Lokal Geliştirme ve Test

1. Depoyu klonlayın veya ZIP şeklinde indirin:

   ```bash
   git clone <REPO_URL>
   cd bc4m-project
   ```

2. (Opsiyonel) Sanal ortam oluşturun ve aktif edin:

   ```bash
   python -m venv venv
   source venv/bin/activate   # Mac/Linux
   # veya
   .\venv\Scripts\activate    # Windows
   
   pip install -r requirements.txt
   ```

3. Flask uygulamasını çalıştırın:

   ```bash
   python app.py
   ```

4. Uygulama 5000 portunda çalışacaktır. Aşağıdaki komutlarla test edebilirsiniz:

   ```bash
   curl http://127.0.0.1:5000/
   # Dönen cevap: {"msg":"BC4M"}

   curl http://127.0.0.1:5000/health
   # Dönen cevap: {"health":"ok"}
   ```

---

## Docker Kullanımı

### Docker Build ve Run (Manuel)

1. **Docker Build**  
   ```bash
   docker build -t bc4m-app:v1 .
   ```

2. **Docker Run**  
   ```bash
   docker run -d --name bc4m-test -p 5000:5000 bc4m-app:v1
   ```

3. **Test**  
   ```bash
   curl http://127.0.0.1:5000/
   # Dönen cevap: {"msg":"BC4M"}

   curl http://127.0.0.1:5000/health
   # Dönen cevap: {"health":"ok"}
   ```

4. **Durdurma ve Silme**  
   ```bash
   docker stop bc4m-test
   docker rm bc4m-test
   ```

### Docker Hub’dan Çekme

Eğer Docker Hub’a push ettiyseniz (örnek kullanıcı adınız `mohitech`), doğrudan çekip kullanabilirsiniz:

```bash
docker pull mohitech/bc4m-app:v1
docker run -d -p 5000:5000 mohitech/bc4m-app:v1
```

> **Not**: `mohitech` yerine kendi Docker Hub kullanıcı adınızı girmeyi unutmayın.

---

## Kubernetes Üzerinde Çalıştırma

### Minikube Kurulumu ve Başlatma

1. Minikube kurulduktan sonra:

   ```bash
   minikube start
   ```

2. Kontrol için:

   ```bash
   kubectl get nodes
   ```
   Tek bir node (minikube) göreceksiniz.

### Deployment ve Service Uygulama

1. **Deployment**:
   ```bash
   kubectl apply -f deployment.yaml
   ```

2. **Service**:
   ```bash
   kubectl apply -f service.yaml
   ```

3. Pod ve Servis durumunu kontrol etmek için:
   ```bash
   kubectl get pods
   kubectl get svc
   ```

### NodePort İle Erişim

`service.yaml` içinde `type: NodePort` tanımlanmışsa:

```yaml
kind: Service
apiVersion: v1
metadata:
  name: bc4m-service
spec:
  type: NodePort
  selector:
    app: bc4m
  ports:
    - port: 80
      targetPort: 5000
      nodePort: 30080
      protocol: TCP
      name: http
```

- `kubectl get svc bc4m-service` komutu ile atanan NodePort’u öğrenin.  
- `minikube ip` komutu ile Minikube IP’sini (örneğin `192.168.49.2`) alın.  
- Ardından şu şekilde test edin:

  ```bash
  curl http://192.168.49.2:30080/
  # Dönen cevap: {"msg":"BC4M"}
  ```

---

## Endpoints Testi

1. **GET /**  
   ```bash
   curl http://<HOST>:<PORT>/
   # Dönen cevap: {"msg":"BC4M"}
   ```

2. **GET /health**  
   ```bash
   curl http://<HOST>:<PORT>/health
   # Dönen cevap: {"health":"ok"}
   ```

3. **POST /**  
   ```bash
   curl -X POST -H "Content-Type: application/json"    -d '{"example":"data"}'    http://<HOST>:<PORT>/
   # Dönen cevap: {"example":"data"}
   ```

> `<HOST>` ve `<PORT>` değerleri, Kubernetes’te Minikube IP + NodePort veya Docker’da `localhost:5000` olabilir.

---

Herhangi bir soru veya sorunda iletişime geçebilirsiniz.

**Teşekkürler ve iyi çalışmalar!**
