<style lang="less">
    @import '../../../styles/common.less';
    @import './case-edit.less';
</style>

<template>
    <div>
        <Row>
            <Col span="18">
                <Card>
                    <Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="80">
                        <FormItem label="Desc" prop="desc">
                            <Input v-model="formValidate.desc" placeholder="Enter case desc" type="textarea" :autosize="{minRows: 2,maxRows: 5}"></Input>
                        </FormItem>
                        <FormItem label="Name" prop="name">
                            <Input v-model="formValidate.name" placeholder="Enter case name"></Input>
                        </FormItem>

                        <FormItem
                                v-for="(itemStep, indexStep) in formValidate.itemsStep"
                                v-if="itemStep.statusStep"
                                :key="indexStep"
                                :label="'Step ' + itemStep.indexStep"
                                :prop="'itemsStep.' + indexStep + '.valueStep'"
                                >
                            <Row>
                                <Col span="18">
                                    <Input type="text" v-model="itemStep.valueStep" placeholder="Enter something..."></Input>
                                </Col>
                                <Col span="4" offset="1">
                                    <Button type="ghost" @click="handleRemoveStep(indexStep)">Delete</Button>
                                </Col>
                            </Row>
                            <FormItem label="Type" prop="type">
                                <RadioGroup v-model="formValidate.type">
                                    <Radio label="0">API</Radio>
                                    <Radio label="1">SQL</Radio>
                                </RadioGroup>
                            </FormItem>
                            <FormItem label="Url">
                                <Row :gutter="8">
                                    <Col span="2">
                                        <FormItem prop="method">
                                            <Select v-model="formValidate.method" placeholder="Get">
                                                <Option value="Get">Get</Option>
                                                <Option value="Post">Post</Option>
                                            </Select>
                                        </FormItem>
                                    </Col>
                                    <Col span="11">
                                        <FormItem prop="path">
                                            <Input v-model="formValidate.path" placeholder="Enter Request path"></Input>
                                        </FormItem>
                                    </Col>
                                    <Col span="5">
                                        <FormItem>
                                            <Button type="primary" @click="selectInterface" >select Interface </Button>
                                        </FormItem>
                                    </Col>
                                </Row>
                            </FormItem>
                            <FormItem label="Header" prop="header">
                                <Input v-model="formValidate.header" type="textarea" :autosize="{minRows: 1,maxRows: 10}"></Input>
                            </FormItem>
                            <FormItem label="Params" prop="params">
                                <Input v-model="formValidate.params" type="textarea" :autosize="{minRows: 2,maxRows: 100}"></Input>
                            </FormItem>
                            <FormItem
                                    v-for="(item, index) in formValidate.items"
                                    v-if="item.status"
                                    :key="index"
                                    :label="'Assert ' + item.index"
                                    :prop="'items.' + index + '.actual'"
                                    :rules="{required: true, message: 'Assert ' + item.index +' can not be empty', trigger: 'blur'}">
                                <Row :gutter="10">
                                    <Col span="8">
                                        <Input type="text" v-model="item.actual" placeholder="Enter actual..."></Input>
                                    </Col>
                                    <Col span="2">
                                        <FormItem prop="rules">
                                            <Select v-model="item.rules" placeholder="=">
                                                <Option value="=">=</Option>
                                                <Option value="!=">!=</Option>
                                                <Option value="<"><</Option>
                                                <Option value=">">></Option>
                                            </Select>
                                        </FormItem>
                                    </Col>
                                    <Col span="8">
                                        <Input type="text" v-model="item.expect" placeholder="Enter expect..."></Input>
                                    </Col>
                                    <Col span="2" offset="1">
                                        <Button type="ghost" @click="handleRemove(index)">Delete</Button>
                                    </Col>
                                </Row>
                            </FormItem>
                            <FormItem>
                                <Row>
                                    <Col span="12">
                                        <Button type="dashed" long @click="handleAdd" icon="plus-round">Add Assert</Button>
                                    </Col>
                                </Row>
                            </FormItem>

                        </FormItem>

                        <FormItem>
                            <Row>
                                <Col span="12">
                                    <Button type="dashed" long @click="handleAddStep" icon="plus-round">Add Step</Button>
                                </Col>
                            </Row>
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
                        <Icon></Icon>&nbsp;&nbsp;状&nbsp;&nbsp;&nbsp; 态：
                        <Select size="small" style="width:90px" value="正常">
                            <Option value=0>正常</Option>
                            <Option value=1>弃用</Option>
                        </Select>
                    </p>
                </Card>
                <div class="margin-top-10">
                    <Card>
                        <p slot="title">
                            <Icon type="navicon-round"></Icon>
                            选择分组
                        </p>
                        <p type="card">
                            <Tree :data="groupList" @on-check-change="setCaseInGroup" show-checkbox ref="tree"></Tree>
                        </p>
                    </Card>
                </div>
                <div class="margin-top-10">
                    <Card>
                        <p slot="title">
                            <Icon type="ios-pricetags-outline"></Icon>
                            调试
                        </p>
                        <Row>
                            <Col span="18">
                                <Select v-model="envSelected" @on-change="handleSelectEnv" placeholder="请选择调试环境，可为空">
                                    <Option v-for="item in envList" :value="item.value" :key="item.value">{{ item.value }}</Option>
                                </Select>
                            </Col>
                            <Col span="6" class="padding-left-10">
                                <Button  @click="handleCase" long type="ghost">调试</Button>
                            </Col>
                        </Row>
                    </Card>
                </div>
            </Col>
        </Row>
    </div>
</template>

<script>
import axios  from 'axios';
export default {
    name: 'artical-publish',
    data () {
        return {
            caseStateList: {status: ''},
            envSelected: [], // 选中的环境
            envList:[], // 所有环境列表


            index: 1,
            indexStep: 1,

            formValidate: {
                    desc: '',
                    name: '',
                    type:'',
                    method: '',
                    path: '',
                    header: '',
                    params: '',
                    items: [
                        {
                            actual: '',
                            expect: '',
                            rules: '',
                            index: 1,
                            status: 1
                        }
                    ],
                    itemsStep: [
                        {
                            valueStep: '',
                            indexStep: 1,
                            statusStep: 1
                        }
                    ]
                },
            ruleValidate: {
                name: [
                        { required: true, message: 'The name cannot be empty', trigger: 'blur' }
                    ],
                desc: [
                        { required: true, message: 'Please enter a personal introduction', trigger: 'blur' },
                        { type: 'string', min: 10, message: 'Introduce no less than 10 words', trigger: 'blur' }
                    ],
                type: [
                        { required: true, message: 'Please select type', trigger: 'change' }
                    ],
                },
            groupList:[],
            selectInterfaceData:{
                name:''
            }
        };
    },
    methods: {
        getData(){
            axios.get("/v1/case/getCaseInfosById",{params:{caseId:this.$route.query.caseId}}
                ).then((res)=>{
                console.log(res)
                if(res.data.success){
                    this.$Message.success("获取数据成功");
                }else{
                    this.$Message.error("获取数据失败")
                }
            });
        },
        getGroupList(){
            axios.get("/v1/group/getGroupByProjectId",{params:{projectId:this.$route.query.projectId,type:1}}).then((res)=>{
                console.log(res);
                if(res.data.success){
                    const that =this;
                    res.data.message.forEach(function(item){
                        console.log(item);
                        that.groupList.push(item);
                    });
                }else{
                    this.$Message.error("获取数据失败")
                }
            })
        },
        getEnv(){
            axios.get("/v1/env/getEnvironmentInfoByUserId",{params:{userId:1}}
                ).then((res)=>{
                console.log(res)
                if(res.data.success){
                    const that = this
                    res.data.message.forEach(function(item){
                        const tmpJson ={}
                        tmpJson["value"]=item["name"]
                        that.envList.push(tmpJson);
                    });
                }else{
                    this.$Message.error("获取数据失败")
                }
            });
        },
        setCaseInGroup(){
        },
        handleCase(){
        },

        handleAdd () {
            this.index++;
            this.formValidate.items.push({
                value: '',
                index: this.index,
                status: 1
            });
        },
        handleRemove (index) {
            this.formValidate.items[index].status = 0;
        },

        handleAddStep () {
                this.indexStep++;
                this.formValidate.itemsStep.push({
                    valueStep: '',
                    indexStep: this.indexStep,
                    statusStep: 1
                });
            },
        handleRemoveStep (indexStep) {
                this.formValidate.itemsStep[indexStep].statusStep = 0;
            },
        handleSelectEnv () {
            localStorage.tagsList = JSON.stringify(this.envSelected);
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
        },
        selectInterface(){
//            this.$Modal.confirm({
//                onOk: () => {
//                       this.selectInterfaceNet();
//                    },
//                    render: (h) => {
//                    return h('div',[
//                        h('Input', {
//                            props: {
//                                value: this.selectInterfaceData.name,
//                                autofocus: true,
//                                placeholder: '接口名称'
//                            },
//                            on: {
//                                input: (val) => {
//                                    this.selectInterfaceData.name = val;
//                                }
//                            }
//                        }),
//                    ])
//                }
//            })
        },
        selectInterfaceNet(){
        },
    },
    created () {
        this.getData();
        this.getEnv();
        this.getGroupList();
    },
};
</script>
