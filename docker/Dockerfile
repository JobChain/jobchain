# docker build -t ubuntu1604py36
FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y software-properties-common vim

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip
RUN apt-get install -y git

RUN apt-get install -y unzip openjdk-8-jre-headless xvfb libxi6 libgconf-2-4 curl wget

RUN CHROME_DRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`
RUN SELENIUM_STANDALONE_VERSION=3.4.0
RUN SELENIUM_SUBDIR=$(echo "$SELENIUM_STANDALONE_VERSION" | cut -d"." -f-2)

RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get -y update
RUN apt-get -y install google-chrome-stable

RUN CHROME_DRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` \
  && wget -N "http://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip" -P ~/
RUN unzip ~/chromedriver_linux64.zip -d ~/
RUN rm ~/chromedriver_linux64.zip
RUN mv -f ~/chromedriver /usr/local/bin/chromedriver
RUN chown root:root /usr/local/bin/chromedriver
RUN chmod 0755 /usr/local/bin/chromedriver

RUN SELENIUM_STANDALONE_VERSION=3.4.0 \
  && SELENIUM_SUBDIR=$(echo "$SELENIUM_STANDALONE_VERSION" | cut -d"." -f-2) \
  &&  wget -N "http://selenium-release.storage.googleapis.com/${SELENIUM_SUBDIR}/selenium-server-standalone-${SELENIUM_STANDALONE_VERSION}.jar" -P ~/ \
  && mv -f ~/selenium-server-standalone-$SELENIUM_STANDALONE_VERSION.jar /usr/local/bin/selenium-server-standalone.jar
RUN chown root:root /usr/local/bin/selenium-server-standalone.jar
RUN chmod 0755 /usr/local/bin/selenium-server-standalone.jar

RUN git clone https://github.com/JobChain/jobchain.git
WORKDIR "/jobchain"
RUN pip3 install -r requirements.txt
WORKDIR "/jobchain/src"
