
ttk.Button(tabloan_right, text="Compute", command=self.progbar).pack()

self.progress = ttk.Progressbar(tabloan_left, orient="horizontal", length=100)
self.progress.pack()
self.progress.config(mode="indeterminate", maximum=100)

self.elapTimeLabel = tk.StringVar()
ttk.Label(tabloan_left, textvariable=self.elapTimeLabel).pack()


def progbar(self, tabloan):
    import time

    self.progress.start(1)
    start_time = time.time()
    tabloan.update_idletasks()  # gui update
    self.compute_payment()  # starts progress (method)
    self.progress.stop()
    end_time = time.time()
    elapsed_time = end_time - start_time
    self.elapTimeLabel.set(format(elapsed_time, '10.3f') + ' s')
