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
                        <FormItem label="requestFormat" prop="format">
                            <RadioGroup v-model="formValidate.format">
                                <Radio label="application/form-data">application/form-data</Radio>
                                <Radio label="application/json">application/json</Radio>
                            </RadioGroup>
                        </FormItem>
                        <FormItem label="responseType" prop="type">
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
                    <p class="margin-top-10">
                        <Icon type="eye"></Icon>&nbsp;&nbsp;公开度：&nbsp;<b>{{ Openness }}</b>
                        <Button v-show="!editOpenness" size="small" @click="handleEditOpenness" type="text">修改</Button>
                        <transition name="openness-con">
                            <div v-show="editOpenness">
                                <RadioGroup v-model="currentOpenness" vertical>
                                    <Radio label="公开">
                                        公开
                                        <Checkbox v-show="currentOpenness === '公开'" v-model="topArticle">在首页置顶这篇文章</Checkbox>
                                    </Radio>
                                    <Radio label="密码">
                                        密码
                                        <Input v-show="currentOpenness === '密码'" style="width:120px" size="small" placeholder="请输入密码"/>
                                    </Radio>
                                    <Radio label="私密"></Radio>
                                </RadioGroup>
                                <div>
                                    <Button type="primary" @click="handleSaveOpenness">确认</Button>
                                    <Button type="ghost" @click="cancelEditOpenness">取消</Button>
                                </div>
                            </div>
                        </transition>
                    </p>
                    <p class="margin-top-10">
                        <Icon type="ios-calendar-outline"></Icon>&nbsp;&nbsp;
                        <span v-if="publishTimeType === 'immediately'">立即发布</span><span v-else>定时：{{ publishTime }}</span>
                        <Button v-show="!editPublishTime" size="small" @click="handleEditPublishTime" type="text">修改</Button>
                        <transition name="publish-time">
                            <div v-show="editPublishTime" class="publish-time-picker-con">
                                <div class="margin-top-10">
                                    <DatePicker @on-change="setPublishTime" type="datetime" style="width:200px;" placeholder="选择日期和时间" ></DatePicker>
                                </div>
                                <div class="margin-top-10">
                                    <Button type="primary" @click="handleSavePublishTime">确认</Button>
                                    <Button type="ghost" @click="cancelEditPublishTime">取消</Button>
                                </div>
                            </div>
                        </transition>
                    </p>
                    <Row class="margin-top-20">
                        <span class="publish-button"><Button @click="handleSaveDraft">编辑</Button></span>
                        <span class="publish-button"><Button @click="handlePublish" :loading="publishLoading" icon="ios-checkmark" style="width:90px;" type="primary">保存</Button></span>
                    </Row>
                </Card>
                <div class="margin-top-10">
                    <Card>
                        <p slot="title">
                            <Icon type="navicon-round"></Icon>
                            分组目录
                        </p>
                        <Tabs type="card">
                            <TabPane label="分组目录">
                                <div class="classification-con">
                                    <Tree :data="classificationList" @on-check-change="setClassificationInAll" show-checkbox></Tree>
                                </div>
                            </TabPane>
                            <TabPane label="子目录">
                                <div class="classification-con">
                                    <CheckboxGroup v-model="offenUsedClassSelected" @on-change="setClassificationInOffen">
                                        <p v-for="item in offenUsedClass" :key="item.title">
                                            <Checkbox :label="item.title">{{ item.title }}</Checkbox>
                                        </p>
                                    </CheckboxGroup>
                                </div>
                            </TabPane>
                        </Tabs>
                    </Card>
                </div>
                <div class="margin-top-10">
                    <Card>
                        <p slot="title">
                            <Icon type="ios-pricetags-outline"></Icon>
                            标签
                        </p>
                        <Row>
                            <Col span="18">
                                <Select v-model="articleTagSelected" multiple @on-change="handleSelectTag" placeholder="请选择文章标签">
                                    <Option v-for="item in articleTagList" :value="item.value" :key="item.value">{{ item.value }}</Option>
                                </Select>
                            </Col>
                            <Col span="6" class="padding-left-10">
                                <Button v-show="!addingNewTag" @click="handleAddNewTag" long type="ghost">新建</Button>
                            </Col>
                        </Row>
                        <transition name="add-new-tag">
                            <div v-show="addingNewTag" class="add-new-tag-con">
                                <Col span="14">
                                    <Input v-model="newTagName" placeholder="请输入标签名" />
                                </Col>
                                <Col span="5" class="padding-left-10">
                                    <Button @click="createNewTag" long type="primary">确定</Button>
                                </Col>
                                <Col span="5" class="padding-left-10">
                                    <Button @click="cancelCreateNewTag" long type="ghost">取消</Button>
                                </Col>
                            </div>
                        </transition>
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
            interfaceStateList: [{value: '正常'}, {value: '禁用'}],
            editOpenness: false,
            Openness: '公开',
            currentOpenness: '公开',
            topArticle: false,
            publishTime: '',
            publishTimeType: 'immediately',
            editPublishTime: false, // 是否正在编辑发布时间
            articleTagSelected: [], // 文章选中的标签
            articleTagList: [], // 所有标签列表
            classificationList: [],
            classificationSelected: [], // 在所有分类目录中选中的目录数组
            offenUsedClass: [],
            offenUsedClassSelected: [], // 常用目录选中的目录
            classificationFinalSelected: [], // 最后实际选择的目录
            publishLoading: false,
            addingNewTag: false, // 添加新标签
            newTagName: '', // 新建标签名

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
                mail: [
                        { required: true, message: 'Mailbox cannot be empty', trigger: 'blur' },
                        { type: 'email', message: 'Incorrect email format', trigger: 'blur' }
                    ],
                city: [
                        { required: true, message: 'Please select the city', trigger: 'change' }
                    ],
                gender: [
                        { required: true, message: 'Please select gender', trigger: 'change' }
                    ],
                interest: [
                        { required: true, type: 'array', min: 1, message: 'Choose at least one hobby', trigger: 'change' },
                        { type: 'array', max: 2, message: 'Choose two hobbies at best', trigger: 'change' }
                    ],
                date: [
                        { required: true, type: 'date', message: 'Please select the date', trigger: 'change' }
                    ],
                time: [
                        { required: true, type: 'date', message: 'Please select time', trigger: 'change' }
                    ],
                desc: [
                        { required: true, message: 'Please enter a personal introduction', trigger: 'blur' },
                        { type: 'string', min: 20, message: 'Introduce no less than 20 words', trigger: 'blur' }
                    ]
                }
        };
    },
    methods: {
        handleEditOpenness () {
            this.editOpenness = !this.editOpenness;
        },
        handleSaveOpenness () {
            this.Openness = this.currentOpenness;
            this.editOpenness = false;
        },
        cancelEditOpenness () {
            this.currentOpenness = this.Openness;
            this.editOpenness = false;
        },
        handleEditPublishTime () {
            this.editPublishTime = !this.editPublishTime;
        },
        handleSavePublishTime () {
            this.publishTimeType = 'timing';
            this.editPublishTime = false;
        },
        cancelEditPublishTime () {
            this.publishTimeType = 'immediately';
            this.editPublishTime = false;
        },
        setPublishTime (datetime) {
            this.publishTime = datetime;
        },
        setClassificationInAll (selectedArray) {
            this.classificationFinalSelected = selectedArray.map(item => {
                return item.title;
            });
            localStorage.classificationSelected = JSON.stringify(this.classificationFinalSelected); // 本地存储所选目录列表
        },
        setClassificationInOffen (selectedArray) {
            this.classificationFinalSelected = selectedArray;
        },
        handleAddNewTag () {
            this.addingNewTag = !this.addingNewTag;
        },
        createNewTag () {
            if (this.newTagName.length !== 0) {
                this.articleTagList.push({value: this.newTagName});
                this.addingNewTag = false;
                setTimeout(() => {
                    this.newTagName = '';
                }, 200);
            } else {
                this.$Message.error('请输入标签名');
            }
        },
        cancelCreateNewTag () {
            this.newTagName = '';
            this.addingNewTag = false;
        },
        canPublish () {
            if (this.articleTitle.length === 0) {
                this.$Message.error('请输入文章标题');
                return false;
            } else {
                return true;
            }
        },
        handleSaveDraft () {
            if (!this.canPublish()) {
                //
            }
        },
        handlePublish () {
            if (this.canPublish()) {
                this.publishLoading = true;
                setTimeout(() => {
                    this.publishLoading = false;
                    this.$Notice.success({
                        title: '保存成功',
                        desc: '文章《' + this.articleTitle + '》保存成功'
                    });
                }, 1000);
            }
        },
        handleSelectTag () {
            localStorage.tagsList = JSON.stringify(this.articleTagSelected); // 本地存储文章标签列表
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
    mounted () {
        this.articleTagList = [
            {value: 'vue'},
            {value: 'iview'},
            {value: 'ES6'},
            {value: 'webpack'},
            {value: 'babel'},
            {value: 'eslint'}
        ];
        this.classificationList = [
            {
                title: 'Vue实例',
                expand: true,
                children: [
                    {
                        title: '数据与方法',
                        expand: true
                    },
                    {
                        title: '生命周期',
                        expand: true
                    }
                ]
            },
            {
                title: 'Class与Style绑定',
                expand: true,
                children: [
                    {
                        title: '绑定HTML class',
                        expand: true,
                        children: [
                            {
                                title: '对象语法',
                                expand: true
                            },
                            {
                                title: '数组语法',
                                expand: true
                            },
                            {
                                title: '用在组件上',
                                expand: true
                            }
                        ]
                    },
                    {
                        title: '生命周期',
                        expand: true
                    }
                ]
            },
            {
                title: '模板语法',
                expand: true,
                children: [
                    {
                        title: '插值',
                        expand: true
                    },
                    {
                        title: '指令',
                        expand: true
                    },
                    {
                        title: '缩写',
                        expand: true
                    }
                ]
            }
        ];
        this.offenUsedClass = [
            {
                title: 'vue实例'
            },
            {
                title: '生命周期'
            },
            {
                title: '模板语法'
            },
            {
                title: '插值'
            },
            {
                title: '缩写'
            }
        ];
        tinymce.init({
            selector: '#articleEditor',
            branding: false,
            elementpath: false,
            height: 600,
            language: 'zh_CN.GB2312',
            menubar: 'edit insert view format table tools',
            theme: 'modern',
            plugins: [
                'advlist autolink lists link image charmap print preview hr anchor pagebreak imagetools',
                'searchreplace visualblocks visualchars code fullscreen fullpage',
                'insertdatetime media nonbreaking save table contextmenu directionality',
                'emoticons paste textcolor colorpicker textpattern imagetools codesample'
            ],
            toolbar1: ' newnote print fullscreen preview | undo redo | insert | styleselect | forecolor backcolor bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image emoticons media codesample',
            autosave_interval: '20s',
            image_advtab: true,
            table_default_styles: {
                width: '100%',
                borderCollapse: 'collapse'
            }
        });
    },
    destroyed () {
        tinymce.get('articleEditor').destroy();
    }
};
</script>
