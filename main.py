from Jobs.Compressor import FileCompressor


def run_job():
    print('New job started')
    d = FileCompressor()
    d.compress()
    print('New job ended')


if __name__ == '__main__':
    run_job()
