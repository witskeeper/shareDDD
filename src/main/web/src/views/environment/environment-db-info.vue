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
                                            <div>
                                                <!-- <Table border :columns="logListColumn" :data="loglist" show-header=false></Table> -->
                                                <ul>
                                                    
                                                    <li v-for="log in loglist" class="margin-bottom-10">
                                                        <Icon type="arrow-right-b"></Icon>
                                                        {{log.content}}
                                                    </li>
                                                </ul>
                                            </div>
                                            
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
            logListColumn: [
                    {
                        title: '信息',
                        key: 'content'
                    },
            ],
            listColumn: [

                    {
                        title: '组名',
                        key: 'name',
                        editable: true,
                    },
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
            loglist: []
        };
    },
    methods: {
        getData() {
            // console.log(this.$route)
            this.DBId = this.$route.query.id
            this.getDatabaseInfoByIdNet()
            this.getTableGroupListNet()
            this.getTableGroupRelationListNet()
            this.getDBLogListByDBIdNet()
        },
        getDBLogListByDBIdNet() {
            axios.get("/v1/table/getDBLogList",
            {"params":{"id": this.DBId}}
            ).then((res)=>{
                if(res.data.success){
                    // this.$Message.success("成功");
                    this.loglist = res.data.message
                }else{
                    this.$Message.error("失败")
                }
            }
            )
        },
        getDatabaseInfoByIdNet() {
            axios.get("/v1/database/getDatabaseInfoById",
            {"params":{"id": this.DBId}}
            ).then((res)=>{
                if(res.data.success){
                    // this.$Message.success("成功");
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
                    // this.$Message.success("成功");
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
                    // this.$Message.success("成功");
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
                    this.$Message.success("编辑成功");
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
                    this.$Message.success("编辑成功");
                    this.getTableGroupListNet()
                }else{
                    this.$Message.error("失败")
                }
            }
            )
        },
        handleDel(val, index) {
            // console.log(val)
            // console.log(index)

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
                    this.$Message.success("新建成功");
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
        deleteGroupNet(index, isDefault, DBId) {
            axios.post("/v1/database/deleteTableGroup",
            {"id": index, "isDefault": isDefault, "DBId": DBId}
            ).then((res)=>{
                if(res.data.success){
                    this.$Message.success("删除成功");
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
            let groups = this.$refs.tree.getCheckedNodes()
            let tables = []
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
                    this.$Message.success("编辑成功");
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
    // created () {
    //     this.getData();
    // },
    beforeRouteEnter(to, from, next) {
    next(vm => {
      vm.getData();
    
    })
  },
};
</script>
