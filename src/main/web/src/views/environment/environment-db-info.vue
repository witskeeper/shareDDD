<style lang="less">
    @import '../../styles/common.less';
    @import './components/table.less';
</style>

<template>
    <div>
        <Row>
            <Col>
                <div class="margin-top-10">
                    <Tabs type="card" @on-click="getData">
                        <TabPane label="数据库详情">
                            <div class="classification-con">
                                <Col span="16">
                                

                                    <Card class="margin-right-10">
                                        <p slot="title">
                                            <Icon type="grid"></Icon>
                                            数据库
                                        </p>
                                        文档详情还差搜索
                                        <p class="margin-bottom-10">数据库名：
                                            <label v-if="editIsHide">{{databaseDataModel.name}}</label>
                                            <Input  v-if="!editIsHide" v-model="databaseDataModel.name" style="width: 300px" ></Input>
                                            </p>
                                        <p class="margin-bottom-10">主机名：
                                            <label v-if="editIsHide">{{databaseDataModel.host}}</label>
                                            <Input  v-if="!editIsHide" v-model="databaseDataModel.host" style="width: 300px" ></Input>
                                            </p>
                                        <p class="margin-bottom-10">端口：
                                            <label v-if="editIsHide">{{databaseDataModel.port}}</label>
                                            <Input  v-if="!editIsHide" v-model="databaseDataModel.port" style="width: 300px" ></Input>
                                            </p>
                                        <p class="margin-bottom-10">用户名：
                                            <label v-if="editIsHide">{{databaseDataModel.username}}</label>
                                            <Input  v-if="!editIsHide" v-model="databaseDataModel.username" style="width: 300px" ></Input>
                                            </p>
                                        <p class="margin-bottom-10">密码：
                                            <label v-if="editIsHide">{{databaseDataModel.password}}</label>
                                            <Input  v-if="!editIsHide" v-model="databaseDataModel.password" style="width: 300px" ></Input>
                                            </p>
                                        <p class="margin-bottom-10">数据库：
                                            <label v-if="editIsHide">{{databaseDataModel.schemaName}}</label>
                                            <Input  v-if="!editIsHide" v-model="databaseDataModel.schemaName" style="width: 300px" ></Input>
                                            </p>
                                        
                                        <p>
                                        <i-button  v-if="editIsHide" type="info" @click="changeEditShow" style="margin-right-10" size="small">编辑</i-button>
                                        <i-button  v-if="!editIsHide" type="success" @click="editDatabase" style="margin-right-10" size="small">保存</i-button>
                                        </p>
                                    </Card>
                                </Col>
                                <Col span="8">
                                    <Card>
                                        <p slot="title">
                                            <Icon type="document"></Icon>
                                            变动记录
                                        </p>
                                    </Card>
                                </Col>
                            </div>
                        </TabPane>
                        <TabPane label="分组设置">
                            <i-button type="success" @click="addGroup" style="margin-top-10">新建分组</i-button>
                            <div class="classification-con">
                                <div class="edittable-table-height-con margin-top-10">
                                    <can-edit-table border :columns-list="listColumn" v-model="listData" @on-delete="handleDel"
                                    :hover-show="true" :edit-incell="true" @on-cell-change="handleCellChange" ></can-edit-table>
                                </div>
                            </div>
                        </TabPane>
                        <TabPane label="表归组设置">
                            <div class="classification-con">
                                <div style="margin-top-10 margin-bottom-10">
                                <i-button type="success" @click="setGroupSelect">设置分组</i-button>
                                </div>
                                <!-- <Card> -->
                                <div style="margin-top-10 margin-bottom-10"><Card>
                                
                                    <Tree ref="tree" :data="groupRelation.groupInfo" show-checkbox></Tree>
                                </Card></div>
                                <!-- </Card> -->
                            </div>
                        </TabPane>
                    </Tabs>
                </div>
            </Col>
        </Row>
                <!-- @on-ok="ok"
        @on-cancel="cancel" -->
        <!-- <div @click="aa">11</div> -->
        <!-- <Modal
        v-model="modal1"
        title="Common Modal dialog box title"

        >
        <RadioGroup v-model="phone">
        <Radio v-for="(item,index) in list" :key="index" label="item.name">
            <span>{{item.name}}</span>
        </Radio>
    </RadioGroup>

    </Modal> -->

    <Modal v-model="setGroupModal" title="设置分组" @on-ok="setGroup">
        <Select v-model="selectValue" style="width:200px">
            <Option v-for="item in listData" :value="item.id" :key="item.id">{{ item.name }}</Option>
        </Select>
    </Modal>
    </div>
</template>

<script>
import canEditTable from './components/canEditTable.vue';
import axios  from 'axios';
export default {
    name: 'environment-db-info',
    components: {
        canEditTable
    },
    data () {
        return {
            treeTableName: "",
            listColumn: [

                    {
                        title: '组名',
                        // width: 120,
                        key: 'name',
                        editable: true,
                    },
                    // {
                    //     title: '操作',
                    //     align: 'center',
                    //     // width: 200,
                    //     key: 'handle',
                    //     handle: ['delete']
                    // }
                    {
                        title: '操作',
                        key: 'id',
                        width: 250,
                        align: 'center',
                        render: (h, params) => {
                            return h('div', [
                                h('Button', {
                                    props: {
                                        type: 'error',
                                        size: 'small'
                                    },
                                    style: {
                                        marginRight: '5px'
                                    },
                                    on: {
                                        click: () => {
                                            this.deleteGroupNet(params.row.id, params.row.isDefault, params.row.DBId)                                  
                                        }
                                    }
                                }, '删除')
                            ])
                        }
                    }
            ],
            listData:[],
            databaseDataModel:{
                    id: 0,
                    name: "",
                    host: "",
                    port: 3306,
                    username: "",
                    password: "",
                    schemaName: "",
                    businessUnit: 2,
                    productUnit: 1,
            },
            groupDataModel:{
                id: 0,
                name: "",
                DBId: 0,
                isDefault: 0
            },
            groupRelation: {
                dbName: "",
                groupInfo: []
            },
            DBId: 0,
            editIsHide: true,
            selectValue:"",
            setGroupModal: false,
        };
    },
    methods: {
        getData() {
            console.log(this.$route)
            this.DBId = this.$route.query.id
            this.getDatabaseInfoByIdNet()
            this.getTableGroupListNet()
            this.getTableGroupRelationListNet()
        },
        getDatabaseInfoByIdNet() {
            axios.get("/v1/database/getDatabaseInfoById",
            {"params":{"id": this.DBId}}
            ).then((res)=>{
                if(res.data.success){
                    this.$Message.success("成功");
                    this.databaseDataModel=res.data.message[0]
                }else{
                    this.$Message.error("失败")
                }
            }
            )
        },
        getTableGroupListNet() {
            axios.get("/v1/database/getTableGroupList",
            {"params":{"id": this.DBId}}
            ).then((res)=>{
                if(res.data.success){
                    this.$Message.success("成功");
                    this.listData=res.data.message
                }else{
                    this.$Message.error("失败")
                }
            }
            )
        },
        getTableGroupRelationListNet() {
            axios.get(
                "/v1/database/getTableGroupRelationList",
                {"params":{"id": this.DBId}}
            ).then((res)=>{
                if(res.data.success){
                    this.groupRelation = res.data.message;
                    this.treeTableName = this.groupRelation.groupInfo[0].children[0].title
                }else{
                    this.$Message.error("失败")
                }
            })
        },
        editDatabaseByIdNet() {
            axios.post("/v1/database/editDatabase",
            this.databaseDataModel
            ).then((res)=>{
                if(res.data.success){
                    this.$Message.success("成功");
                    this.getDatabaseInfoByIdNet()
                }else{
                    this.$Message.error("失败")
                }
            }
            )
        },
        editDatabase() {
            this.changeEditShow()
            this.editDatabaseByIdNet()
        },
        changeEditShow() {
            this.editIsHide = !this.editIsHide
        },
        handleCellChange(val, index, key) {
            console.log(val)
            this.groupDataModel.DBId = val[index]["DBId"]
            this.groupDataModel.name = val[index]["name"]
            this.groupDataModel.id = val[index]["id"]
            this.editGroupByIdNet()
        },
        editGroupByIdNet() {
            axios.post("/v1/database/editTableGroup",
            this.groupDataModel
            ).then((res)=>{
                if(res.data.success){
                    this.$Message.success("成功");
                    this.getTableGroupListNet()
                }else{
                    this.$Message.error("失败")
                }
            }
            )
        },
        handleDel(val, index) {
            console.log(val)
            console.log(index)

        },
        addGroup() {
            this.initGroupDataModel()
            this.$Modal.confirm({
                onOk: () => {
                       this.addGroupNet();
                    },
                    render: (h) => {
                    return h('div',[
                        h('Input', {
                            props: {
                                value: this.groupDataModel.name,
                                autofocus: true,
                                placeholder: '组名'
                            },
                            on: {
                                input: (val) => {
                                    this.groupDataModel.name = val;
                                    this.groupDataModel.DBId = this.DBId;
                                    this.groupDataModel.isDefault = 0
                                }
                            }
                        }),
                    ])
                }
            })
        },
        addGroupNet() {
            axios.post("/v1/database/addTableGroup",
            this.groupDataModel
            ).then((res)=>{
                if(res.data.success){
                    this.$Message.success("成功");
                    this.getTableGroupListNet()
                }else{
                    this.$Message.error("失败")
                }
            }
            )
        },
        initGroupDataModel() {
            this.groupDataModel = {
                    id: 0,
                    name: "",
                    DBId: 0,
                    isDefault: 0
            }
        },
        deleteGroup(val) {
            console.log(val)
        },
        deleteGroupNet(index, isDefault, DBId) {
            axios.post("/v1/database/deleteTableGroup",
            {"id": index, "isDefault": isDefault, "DBId": DBId}
            ).then((res)=>{
                if(res.data.success){
                    this.$Message.success("成功");
                    this.getTableGroupListNet()
                }else{
                    this.$Message.error("失败")
                }
            }
            )
        },
        setGroupSelect() {
            this.setGroupModal = true
        },
        setGroup() {
            this.setGroupModal = false
            const groups = this.$refs.tree.getCheckedNodes()
            console.log(groups)
            var tables = []
            for(var i=0;i<groups.length;i++) {
                if(groups[i].children === undefined) {
                    tables.push((groups[i].id).toString())
                }
            }
            // 传入表名数组
            this.updateTableGroupRelationNet(tables, this.selectValue)           
        },
        updateTableGroupRelationNet(tables, groupId) {
            axios.post("/v1/database/updateTableGroupRelation",
            {"tables": tables, "DBId": this.DBId, "groupId": groupId}
            ).then((res)=>{
                if(res.data.success){
                    this.$Message.success("成功");
                    this.getTableGroupRelationListNet()
                }else{
                    this.$Message.error("失败")
                }
            }
            )
        },
        
    },
    mounted () {
        // this.getData();
    },
    created () {
        this.getData();
    }
};

// import tinymce from 'tinymce';
// export default {
//     name: 'artical-publish',
//     data () {
//         return {
//             articleTitle: '',
//             articleError: '',
//             showLink: false,
//             fixedLink: '',
//             articlePath: '',
//             articlePathHasEdited: false,
//             editLink: false,
//             editPathButtonType: 'ghost',
//             editPathButtonText: '编辑',
//             articleStateList: [{value: '草稿'}, {value: '等待复审'}],
//             editOpenness: false,
//             Openness: '公开',
//             currentOpenness: '公开',
//             topArticle: false,
//             publishTime: '',
//             publishTimeType: 'immediately',
//             editPublishTime: false, // 是否正在编辑发布时间
//             articleTagSelected: [], // 文章选中的标签
//             articleTagList: [], // 所有标签列表
//             classificationList: [],
//             classificationSelected: [], // 在所有分类目录中选中的目录数组
//             offenUsedClass: [],
//             offenUsedClassSelected: [], // 常用目录选中的目录
//             classificationFinalSelected: [], // 最后实际选择的目录
//             publishLoading: false,
//             addingNewTag: false, // 添加新标签
//             newTagName: '' // 新建标签名
//         };
//     },
//     methods: {
//         handleArticletitleBlur () {
//             if (this.articleTitle.length !== 0) {
//                 // this.articleError = '';
//                 localStorage.articleTitle = this.articleTitle; // 本地存储文章标题
//                 if (!this.articlePathHasEdited) {
//                     let date = new Date();
//                     let year = date.getFullYear();
//                     let month = date.getMonth() + 1;
//                     let day = date.getDate();
//                     this.fixedLink = window.location.host + '/' + year + '/' + month + '/' + day + '/';
//                     this.articlePath = this.articleTitle;
//                     this.articlePathHasEdited = true;
//                     this.showLink = true;
//                 }
//             } else {
//                 // this.articleError = '文章标题不可为空哦';
//                 this.$Message.error('文章标题不可为空哦');
//             }
//         },
//         editArticlePath () {
//             this.editLink = !this.editLink;
//             this.editPathButtonType = this.editPathButtonType === 'ghost' ? 'success' : 'ghost';
//             this.editPathButtonText = this.editPathButtonText === '编辑' ? '完成' : '编辑';
//         },
//         handleEditOpenness () {
//             this.editOpenness = !this.editOpenness;
//         },
//         handleSaveOpenness () {
//             this.Openness = this.currentOpenness;
//             this.editOpenness = false;
//         },
//         cancelEditOpenness () {
//             this.currentOpenness = this.Openness;
//             this.editOpenness = false;
//         },
//         handleEditPublishTime () {
//             this.editPublishTime = !this.editPublishTime;
//         },
//         handleSavePublishTime () {
//             this.publishTimeType = 'timing';
//             this.editPublishTime = false;
//         },
//         cancelEditPublishTime () {
//             this.publishTimeType = 'immediately';
//             this.editPublishTime = false;
//         },
//         setPublishTime (datetime) {
//             this.publishTime = datetime;
//         },
//         setClassificationInAll (selectedArray) {
//             this.classificationFinalSelected = selectedArray.map(item => {
//                 return item.title;
//             });
//             localStorage.classificationSelected = JSON.stringify(this.classificationFinalSelected); // 本地存储所选目录列表
//         },
//         setClassificationInOffen (selectedArray) {
//             this.classificationFinalSelected = selectedArray;
//         },
//         handleAddNewTag () {
//             this.addingNewTag = !this.addingNewTag;
//         },
//         createNewTag () {
//             if (this.newTagName.length !== 0) {
//                 this.articleTagList.push({value: this.newTagName});
//                 this.addingNewTag = false;
//                 setTimeout(() => {
//                     this.newTagName = '';
//                 }, 200);
//             } else {
//                 this.$Message.error('请输入标签名');
//             }
//         },
//         cancelCreateNewTag () {
//             this.newTagName = '';
//             this.addingNewTag = false;
//         },
//         canPublish () {
//             if (this.articleTitle.length === 0) {
//                 this.$Message.error('请输入文章标题');
//                 return false;
//             } else {
//                 return true;
//             }
//         },
//         handlePreview () {
//             if (this.canPublish()) {
//                 if (this.publishTimeType === 'immediately') {
//                     let date = new Date();
//                     let year = date.getFullYear();
//                     let month = date.getMonth() + 1;
//                     let day = date.getDate();
//                     let hour = date.getHours();
//                     let minute = date.getMinutes();
//                     let second = date.getSeconds();
//                     localStorage.publishTime = year + ' 年 ' + month + ' 月 ' + day + ' 日 -- ' + hour + ' : ' + minute + ' : ' + second;
//                 } else {
//                     localStorage.publishTime = this.publishTime; // 本地存储发布时间
//                 }
//                 localStorage.content = tinymce.activeEditor.getContent();
//                 this.$router.push({
//                     name: 'preview'
//                 });
//             }
//         },
//         handleSaveDraft () {
//             if (!this.canPublish()) {
//                 //
//             }
//         },
//         handlePublish () {
//             if (this.canPublish()) {
//                 this.publishLoading = true;
//                 setTimeout(() => {
//                     this.publishLoading = false;
//                     this.$Notice.success({
//                         title: '保存成功',
//                         desc: '文章《' + this.articleTitle + '》保存成功'
//                     });
//                 }, 1000);
//             }
//         },
//         handleSelectTag () {
//             localStorage.tagsList = JSON.stringify(this.articleTagSelected); // 本地存储文章标签列表
//         }
//     },
//     computed: {
//         completeUrl () {
//             let finalUrl = this.fixedLink + this.articlePath;
//             localStorage.finalUrl = finalUrl; // 本地存储完整文章路径
//             return finalUrl;
//         }
//     },
//     mounted () {
//         this.articleTagList = [
//             {value: 'vue'},
//             {value: 'iview'},
//             {value: 'ES6'},
//             {value: 'webpack'},
//             {value: 'babel'},
//             {value: 'eslint'}
//         ];
//         this.classificationList = [
//             {
//                 title: 'Vue实例',
//                 expand: true,
//                 children: [
//                     {
//                         title: '数据与方法',
//                         expand: true
//                     },
//                     {
//                         title: '生命周期',
//                         expand: true
//                     }
//                 ]
//             },
//             {
//                 title: 'Class与Style绑定',
//                 expand: true,
//                 children: [
//                     {
//                         title: '绑定HTML class',
//                         expand: true,
//                         children: [
//                             {
//                                 title: '对象语法',
//                                 expand: true
//                             },
//                             {
//                                 title: '数组语法',
//                                 expand: true
//                             },
//                             {
//                                 title: '用在组件上',
//                                 expand: true
//                             }
//                         ]
//                     },
//                     {
//                         title: '生命周期',
//                         expand: true
//                     }
//                 ]
//             },
//             {
//                 title: '模板语法',
//                 expand: true,
//                 children: [
//                     {
//                         title: '插值',
//                         expand: true
//                     },
//                     {
//                         title: '指令',
//                         expand: true
//                     },
//                     {
//                         title: '缩写',
//                         expand: true
//                     }
//                 ]
//             }
//         ];
//         this.offenUsedClass = [
//             {
//                 title: 'vue实例'
//             },
//             {
//                 title: '生命周期'
//             },
//             {
//                 title: '模板语法'
//             },
//             {
//                 title: '插值'
//             },
//             {
//                 title: '缩写'
//             }
//         ];
//         tinymce.init({
//             selector: '#articleEditor',
//             branding: false,
//             elementpath: false,
//             height: 600,
//             language: 'zh_CN.GB2312',
//             menubar: 'edit insert view format table tools',
//             theme: 'modern',
//             plugins: [
//                 'advlist autolink lists link image charmap print preview hr anchor pagebreak imagetools',
//                 'searchreplace visualblocks visualchars code fullscreen fullpage',
//                 'insertdatetime media nonbreaking save table contextmenu directionality',
//                 'emoticons paste textcolor colorpicker textpattern imagetools codesample'
//             ],
//             toolbar1: ' newnote print fullscreen preview | undo redo | insert | styleselect | forecolor backcolor bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image emoticons media codesample',
//             autosave_interval: '20s',
//             image_advtab: true,
//             table_default_styles: {
//                 width: '100%',
//                 borderCollapse: 'collapse'
//             }
//         });
//     },
//     destroyed () {
//         tinymce.get('articleEditor').destroy();
//     }
// };
</script>
