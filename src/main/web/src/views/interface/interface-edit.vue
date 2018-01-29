<style lang="less">
    @import '../../styles/common.less';
    @import './interface-edit.less';
</style>

<template>
    <div>
        <Row>
            <Col span="18">
                <Card>
                    <Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="80">
                        <FormItem label="Name" prop="name">
                            <Input v-model="formValidate.name" placeholder="Enter interface name"></Input>
                        </FormItem>
                        <FormItem label="URL" prop="url">
                            <Input v-model="formValidate.url" placeholder="Enter interface url"></Input>
                        </FormItem>
                        <FormItem label="Method" prop="method">
                            <Select v-model="formValidate.method" placeholder="Select interface method">
                                <Option value="Get">Get</Option>
                                <Option value="Post">Post</Option>
                            </Select>
                        </FormItem>
                        <FormItem label="Format" prop="format">
                            <RadioGroup v-model="formValidate.format">
                                <Radio label="application/form-data">application/form-data</Radio>
                                <Radio label="application/json">application/json</Radio>
                            </RadioGroup>
                        </FormItem>
                        <FormItem label="Type" prop="type">
                            <RadioGroup v-model="formValidate.type">
                                <Radio label="json">json</Radio>
                                <Radio label="view">view</Radio>
                            </RadioGroup>
                        </FormItem>
                        <FormItem label="Params" prop="params">
                            <Input v-model="formValidate.params" type="textarea" :autosize="{minRows: 2,maxRows: 100}" placeholder="Request params..."></Input>
                        </FormItem>
                        <FormItem label="Success" prop="success">
                            <Input v-model="formValidate.success" type="textarea" :autosize="{minRows: 2,maxRows: 100}" placeholder="Success response..."></Input>
                        </FormItem>
                        <FormItem label="Failure" prop="failure">
                            <Input v-model="formValidate.failure" type="textarea" :autosize="{minRows: 2,maxRows: 100}" placeholder="Failure response..."></Input>
                        </FormItem>
                        <FormItem label="Desc" prop="desc">
                            <Input v-model="formValidate.desc" type="textarea" :autosize="{minRows: 2,maxRows: 50}" placeholder="Enter your describe..."></Input>
                        </FormItem>
                        <FormItem>
                            <Button type="primary" @click="handleSubmit('formValidate')">Submit</Button>
                            <Button type="ghost" @click="handleReset('formValidate')" style="margin-left: 8px">Reset</Button>
                        </FormItem>
                    </Form>
                </Card>
            </Col>
            <Col span="6" class="padding-left-10">
                <Card>
                    <p slot="title">
                        <Icon type="paper-airplane"></Icon>
                        设置
                    </p>
                    <p class="margin-top-10">
                        <Icon type="android-time"></Icon>&nbsp;&nbsp;状&nbsp;&nbsp;&nbsp; 态：
                        <Select size="small" style="width:90px" value="正常">
                            <Option v-for="item in interfaceStateList" :value="item.value" :key="item.value">{{ item.value }}</Option>
                        </Select>
                    </p>
                    <Row class="margin-top-20">
                        <span class="publish-button"><Button @click="handlePublish" style="width:90px;" type="primary">保存</Button></span>
                    </Row>
                </Card>
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
import tinymce from 'tinymce';
export default {
    name: 'artical-publish',
    data () {
        return {
            interfaceStateList: [{value: '正常'}, {value: '废弃'}],
            formValidate: {
                    name: '',
                    url: '',
                    method: '',
                    format: '',
                    type: '',
                    params: '',
                    success: '',
                    failure:'',
                    desc: ''
                },
            ruleValidate: {
                name: [
                        { required: true, message: 'The name cannot be empty', trigger: 'blur' }
                    ],
                url: [
                        { required: true, message: 'The url cannot be empty', trigger: 'blur' }
                    ],
                method: [
                        { required: true, message: 'The method cannot be empty', trigger: 'blur' }
                    ],
                success: [
                        { required: true, message: 'The success cannot be empty', trigger: 'blur' }
                    ],
                type: [
                        { required: true, message: 'Please select type', trigger: 'change' }
                    ],
                format: [
                        { required: true, message: 'Please select format', trigger: 'change' }
                    ],
                desc: [
                        { required: true, message: 'Please enter a personal introduction', trigger: 'blur' },
                        { type: 'string', min: 10, message: 'Introduce no less than 10 words', trigger: 'blur' }
                    ]
                }
        };
    },
    methods: {
        handlePublish () {

        },
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
