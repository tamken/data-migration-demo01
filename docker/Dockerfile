FROM mysql:8.0

RUN apt-get update && apt-get install -y locales \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/* \
	&& echo "ja_JP.UTF-8 UTF-8" > /etc/locale.gen \
	&& locale-gen ja_JP.UTF-8

ENV LC_ALL ja_JP.UTF-8
ENV TZ=Aaia/Tokyo

COPY ./conf/custom.cnf /etc/mysql/conf.d
