from crontab import CronTab

my_cron = CronTab(user='ivan')
job = my_cron.new(command=r'rm -f /home/ivan/Рабочий\ стол/hack/hack.log &'
                          r' cat > /home/ivan/Рабочий\ стол/hack/hack.log')
job.minute.every(1)
my_cron.write()
