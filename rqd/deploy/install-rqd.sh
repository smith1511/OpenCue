#!/bin/bash -e

PYTHON_VERSION="2.7.17"
RQD_VERSION="0.3.6"
SCRIPT=`basename ${BASH_SOURCE[0]}`


function usage {
  echo "Basic usage: $SCRIPT -c 10.0.0.1 -v 0.3.6"
  echo ""
  echo "-c   --Sets the Cuebot hostname or IP address.  Required."
  echo "-v   --Sets the RQD version.  Optional."
  exit 1
}


while getopts c:v:h FLAG; do
  case $FLAG in
    c)
      CUEBOT_HOSTNAME=$OPTARG
      ;;
    v)
      RQD_VERSION=$OPTARG
      ;;
    h)
      usage
      ;;
    \?)
      echo "Option -$OPTARG not recognized."
      usage
      ;;
  esac
done


if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi


if [[ ! -r "/etc/redhat-release" ]]; then
    echo "Currently this script only supports Red Hat and CentOS Linux distributions."
    exit 1
fi


if [[ -z "$CUEBOT_HOSTNAME" ]]; then
    echo "Cuebot hostname or IP address is not set."
    exit 1
fi


function install_python {

    # Install dependencies required to build Python
    yum install -y gcc openssl-devel bzip2-devel
    
    PYTHON_PREFIX="/opt/opencue/python"
    mkdir -p $PYTHON_PREFIX

    # Download and install Python
    wget -O Python-${PYTHON_VERSION}.tgz "https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz"
    tar xvfz Python-${PYTHON_VERSION}.tgz
    pushd Python-${PYTHON_VERSION}
    ./configure --enable-optimizations --prefix /opt/opencue/python

    # Installs to $PYTHON_PREFIX/bin/python2.7
    make altinstall
    popd
    rm -rf Python-${PYTHON_VERSION}*

    # Install PyPi
    wget -O /tmp/get-pip.py "https://bootstrap.pypa.io/get-pip.py"
    $PYTHON_PREFIX/bin/python2.7 /tmp/get-pip.py
}


function install_rqd {

    # Download RQD
    wget -O rqd-${RQD_VERSION}-all.tar.gz "https://github.com/AcademySoftwareFoundation/OpenCue/releases/download/${RQD_VERSION}/rqd-${RQD_VERSION}-all.tar.gz"
    tar xvfz rqd-${RQD_VERSION}-all.tar.gz
    pushd rqd-${RQD_VERSION}-all

    # Install the Python deps
    $PYTHON_PREFIX/bin/pip2.7 install -r requirements.txt
    $PYTHON_PREFIX/bin/python2.7 setup.py install
    ln -f -s $PYTHON_PREFIX/bin/rqd /usr/bin/rqd
    
    # Install the Systemd service script
    cp deploy/opencue-rqd.service /etc/systemd/system
    popd
    rm -rf rqd-${RQD_VERSION}-all*

    # Set the Cuebot hostname
    echo "CUEBOT_HOSTNAME=${CUEBOT_HOSTNAME}" > /etc/sysconfig/opencue-rqd

    # Start the service
    systemctl daemon-reload
    systemctl enable opencue-rqd
    systemctl start opencue-rqd
}

install_python

install_rqd
