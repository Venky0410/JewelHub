# JewelHub 💍

A cloud-native microservices e-commerce platform 
for handcrafted silver jewellery — built with 
    Python Flask, Docker, and Kubernetes.

    ---

## 🚀 Live Demo
http://ab8acc5a05ba547a3a09a6a4c54c90bd-432019217.eu-west-1.elb.amazonaws.com

---

## ✅ Project Status
- ✅ JewelHub running on AWS EKS
- ✅ Public URL accessible
- ✅ 6 microservices running
- ✅ High availability (2 pods each)
- ✅ Multi-AZ deployment
- ✅ Load balanced traffic
- ✅ Health checks running
- ✅ Auto-restart on failure

---

## 🏗️ Architecture
```
User → Load Balancer → Frontend (5000)
                            ↓
               ┌────────────┼────────────┐
               ↓            ↓            ↓
        Product (5001)  Cart (5002)  Order (5003)
                            ↓
                    User (5004)
                            ↓
                Notification (5005)
```




---

## 🛠️ Tech Stack
| Layer | Technology |
|---|---|
| Language | Python Flask |
| Container | Docker |
| Registry | AWS ECR |
| Orchestration | Kubernetes (AWS EKS) |
| Cloud | AWS (eu-west-1) |
| Architecture | Microservices |

---

## 📦 Microservices
| Service | Port | Purpose |
|---|---|---|
| Frontend | 5000 | UI — Homepage, Products, Cart |
| Product Service | 5001 | Jewellery catalogue API |
| Cart Service | 5002 | Shopping cart API |
| Order Service | 5003 | Order management API |
| User Service | 5004 | Authentication API |
| Notification Service | 5005 | Order notifications |

---

## 🚀 Deployment
Built and deployed using:
- Docker images pushed to AWS ECR
- Kubernetes manifests in /k8s folder
- Deployed to AWS EKS cluster
- Monitored by SteadyStackAI

---

## 📊 SRE Platform
This app is monitored by 
**[SteadyStackAI](https://github.com/Venky0410/steadystackAI)**
— a production-grade SRE platform with:
- Prometheus + Grafana monitoring
- ELK Stack logging
- Chaos Engineering
- AI-powered incident management

---

## 👨💻 Author
**Venkatesh Saggam**
- GitHub: Venky0410
- Email: venkysaggam5@gmail.com