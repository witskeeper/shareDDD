<style lang="less">
    @import '../../styles/common.less';
    @import './environment-info.less';
</style>

<template>
    <div>
        <Row>
            <Col span="18">
                <Card>
                    <Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="80">
                        <FormItem label="环境名称" prop="name">
                            <Input v-model="formValidate.name" placeholder="Enter environment name"></Input>
                        </FormItem>
                        <FormItem label="前置URL" prop="url">
                            <Input v-model="formValidate.url" placeholder="Enter url"></Input>
                        </FormItem>
                        <FormItem label="数据模板" prop="data">
                            <Input v-model="formValidate.data" type="textarea" :autosize="{minRows: 2,maxRows: 100}" placeholder="Data template..."></Input>
                        </FormItem>
                        <FormItem label="DB名称" prop="DBname">
                            <Input v-model="formValidate.DBname" placeholder="DataBase name..."></Input>
                        </FormItem>
                        <FormItem label="HostName" prop="hostName">
                            <Input v-model="formValidate.hostName" placeholder="DataBase hostName..."></Input>
                        </FormItem>
                        <FormItem label="Port" prop="port">
                            <Input v-model="formValidate.port" placeholder="DataBase port..."></Input>
                        </FormItem>
                        <FormItem label="UserName" prop="userName">
                            <Input v-model="formValidate.desc" placeholder="DataBase userName..."></Input>
                        </FormItem>
                        <FormItem label="PassWord" prop="passWord">
                            <Input v-model="formValidate.passWord" placeholder="DataBase passWord..."></Input>
                        </FormItem>
                        <FormItem>
                            <Button type="primary" @click="handleSubmit('formValidate')">Submit</Button>
                            <Button type="ghost" @click="handleReset('formValidate')" style="margin-left: 8px">Reset</Button>
                        </FormItem>
                    </Form>
                </Card>
            </Col>
            <Col span="6" class="padding-left-10">
                <div class="margin-top-10">
                    <Card>
                        <p slot="title">
                            <Icon type="navicon-round"></Icon>
                            修改记录
                        </p>
                    </Card>
                </div>
            </Col>
        </Row>
    </div>
</template>

<script>
export default {
    name: 'environment-info',
    data () {
        return {
            formValidate: {
                    name: '',
                    url: '',
                    data: '',
                    DBname: '',
                    hostName:'',
                    port: '',
                    userName: '',
                    passWord: ''
                },
            ruleValidate: {
                name: [
                        { required: true, message: 'The name cannot be empty', trigger: 'blur' }
                    ],
                url: [
                        { required: true, message: 'The url cannot be empty', trigger: 'blur' }
                    ],
                data: [
                        { required: true, message: 'Please enter the test data template', trigger: 'blur' },
                        { type: 'string', min: 10, message: 'Introduce no less than 10 words', trigger: 'blur' }
                    ]
                }
        };
    },
    methods: {
        handleSubmit (name) {
            this.$refs[name].validate((valid) => {
                if (valid) {
                    this.$Message.success('Success!');
                } else {
                    this.$Message.error('Fail!');
                }
            })
        },
        handleReset (name) {
            this.$refs[name].resetFields();
        }
    },
};
</script>
