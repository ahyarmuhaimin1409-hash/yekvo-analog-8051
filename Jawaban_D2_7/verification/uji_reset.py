for test_id, clock_siap_us in [("T01-B", 5), ("T01-F", 7)]:
    durasi_us = 0
    for t in range(10):
        rst_high = t < 8
        clock_siap = t >= clock_siap_us
        if rst_high and clock_siap:
            durasi_us += 1

    hasil = "LULUS" if durasi_us >= 2 else "GAGAL"
    print(f"{test_id}: {durasi_us} us -> {hasil}")
