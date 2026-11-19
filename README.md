# HMQTF

ชุดโค้ด Python สำหรับทดลองเชิงตัวเลขเกี่ยวกับพลวัตของระบบควอนตัมมิติจำกัด โดยมีคลาสหลัก `HMQTF` สำหรับสร้างสถานะและเมทริกซ์ความหนาแน่น จำลองวิวัฒนาการแบบ Lindblad คำนวณค่าตรวจวัดเชิงวินิจฉัย และทดลองฟังก์ชันที่เกี่ยวกับลำดับ Fibonacci และ limit cycle

> **ขอบเขต:** README นี้อธิบายสิ่งที่โค้ดใน repository ทำอยู่ ไม่ได้ยืนยันว่าการจำลองเป็นกลไก quantum error correction ที่ผ่านการพิสูจน์หรือผ่านการตรวจสอบทางฟิสิกส์แล้ว

**ผู้พัฒนา:** Chutiphong Bunloed (Buriram, Thailand)  
**ORCID:** [0009-0003-4295-7521](https://orcid.org/0009-0003-4295-7521)  
**Email:** synthesis496@gmail.com

## โครงสร้าง repository

- `hmqtf_product.py` — คลาส `HMQTF` และฟังก์ชันหลักของแบบจำลอง
- `hmqtf_demo.py` — ตัวอย่างการเรียกใช้: วิวัฒนาการสถานะ, batch, infinite extension, limit cycle และ Fibonacci
- `hmqtf_test.py` — ชุดฟังก์ชันทดสอบ โดย `run_all()` คืนค่า Boolean ของแต่ละกรณี
- `hmqtf_benchmark.py` — ฟังก์ชัน benchmark สำหรับการดำเนินการและการจำลองหลายรูปแบบ

## ความสามารถในโค้ด

คลาส `HMQTF` รับพารามิเตอร์ `d`, `gamma`, `hbar`, `tau_0`, `C`, `beta` และ `a` โดยมีค่าเริ่มต้นตาม constructor ใน `hmqtf_product.py` โค้ดประกอบด้วย:

- สร้าง computational basis state ด้วย `fermison()` และ `fermison_batch()` และแปลงเป็น density matrix
- คำนวณ mirror, fold, conservation scalar และ anti-cascade metric รวมถึง mirror/parity action บน state
- สร้าง Fibonacci sequence, Fibonacci clock และค่าความคลาดเคลื่อนของอัตราส่วน Fibonacci ต่อ golden ratio
- จำลอง evolution ด้วย `evolve_fast()` (Euler แบบขั้นเวลา), `evolve_accurate()` (SciPy `solve_ivp`/RK45), และ `evolve_batch()`; `evolve_multi_gamma()` จำลองหลายค่า gamma
- คำนวณ purity, entropy, fermion number, stabilizer, trace distance, expected/effective energy และ spectral diagnostics
- บันทึก/โหลด configuration ด้วย `save()`/`load()` และสร้าง instance ใหม่ด้วย `clone()`

`hmqtf_demo.py` แสดงตัวอย่างการใช้งานเหล่านี้ แต่การมีฟังก์ชันในโค้ดไม่ได้หมายความว่าผลลัพธ์ได้รับการยืนยันเชิงทฤษฎีหรือเชิงทดลองแล้ว

## ติดตั้งและเริ่มต้นใช้งาน

ต้องใช้ Python และ dependencies ต่อไปนี้:

```bash
python -m pip install numpy scipy
```

หลัง clone repository แล้ว ให้รันคำสั่งจากไดเรกทอรีของ repository:

```bash
python -c "import hmqtf_demo; print(hmqtf_demo.demo())"
```

ตัวอย่างใช้งานคลาสโดยตรง:

```python
import hmqtf_product

model = hmqtf_product.HMQTF(d=8, gamma=0.05)
state = model.fermison(0)
result = model.run(state, n_steps=2000, dt=0.0005)

print("purity:", result["purity"])
print("trace error:", result["trace_error"])
```

เรียกชุดทดสอบที่มีใน repository ได้ด้วย:

```bash
python -c "import hmqtf_test; results = hmqtf_test.run_all(); print(results); print(f'{sum(results)}/{len(results)} passed')"
```

`run_all()` คืน list ของผล Boolean; คำสั่งด้านบนจึงแสดงผลรายกรณีและจำนวนกรณีที่ผ่าน ไม่ใช่การเรียกใช้ pytest

## หมายเหตุเกี่ยวกับการตีความผล

- `evolve_fast()` ใช้ Euler time stepping และปรับ trace ให้เป็น 1 ในแต่ละ step ส่วน `evolve_accurate()` ใช้ RK45 และคืน trajectory ตาม `n_points` ที่กำหนด
- ใน implementation ปัจจุบัน ตัว dissipator สร้าง jump operator จาก `sqrt(gamma)` และยังคูณ dissipator ด้วย `gamma` ในสมการ evolution ด้วย ดังนั้นผลจาก gamma ขึ้นกับการประกอบสองส่วนนี้ ควรตรวจสอบสมการและ convention ของพารามิเตอร์ก่อนนำผลไปตีความทางกายภาพ
- `HMQTF` เป็นชื่อคลาส/แบบจำลองในโค้ด; ฟังก์ชันที่มีชื่อเกี่ยวกับ correction, conservation หรือ stabilizer ไม่ได้ด้วยตัวเองพิสูจน์คุณสมบัติการแก้ข้อผิดพลาดหรือการอนุรักษ์ตามความหมายทางฟิสิกส์
- `hmqtf_benchmark.py` มี benchmark functions แต่ README นี้ไม่กล่าวอ้างผลด้านประสิทธิภาพหรือ scaling ที่ผ่านการวัดและยืนยันแล้ว

## Citation

Chutiphong. (2026). synthesis496/hmqtf: update full (Version v2.2.1) [Computer software]. Zenodo. https://doi.org/10.5281/zenodo.24369802

## License

GNU Affero General Public License v3.0 (AGPL-3.0) — ดูรายละเอียดในไฟล์ `LICENSE`.
