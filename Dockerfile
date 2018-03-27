FROM 209983464176.dkr.ecr.us-east-1.amazonaws.com/ansible 

ADD . /tmp/playbook
WORKDIR /tmp/playbook

## run tests
RUN ansible-playbook -vvvv -i "[test] localhost," -c local test.yml -e "environ=dev" &&\
    IDEMPOTENCE_RESULT=$( ansible-playbook -i "[test] localhost," -c local test.yml -e "environ=dev" 2>/dev/null ) &&\
    echo $IDEMPOTENCE_RESULT | grep -q 'changed=0.*failed=0' &&\
    (echo 'Idempotence test: \033[0;32mpass\033[0m' && exit 0) ||\
    (echo 'Idempotence test: \033[0;31mfail\033[0m' && echo "$IDEMPOTENCE_RESULT" && exit 1)

CMD /bin/bash
