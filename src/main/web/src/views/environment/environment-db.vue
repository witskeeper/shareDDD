<style lang="less">
    @import '../../styles/common.less';
    @import './components/table.less';
</style>

<template>
    <div>
        <Row type="flex" class="height-100">
            <Col span="8">
                <i-button type="success" @click="addDatabase" style="margin-top-10">新建数据库</i-button>
            </Col>
        </Row>
        <Row class="margin-top-10">
            <Col>
                <!-- <Card> -->
                    <div class="edittable-table-height-con">
                        <Table border :columns="listColumn" :data="list"></Table>
                    </div>
                <!-- </Card> -->
            </Col>
        </Row>
    </div>
</template>

<script>
import axios  from 'axios';
export default {
    name: 'enviroment-db',
    data () {
        return {
            listColumn: [

                    {
                        title: '数据库名',
                        key: 'name'
                    },
                    {
                        title: '主机名',
                        key: 'host'
                    },
                    {
                        title: '端口',
                        key: 'port'
                    },
                    {
                        title: '用户名',
                        key: 'username'
                    },
                    //不暴露在外面
                    // {
                    //     title: '密码',
                    //     key: 'password'
                    // },
                    {
                        title: '数据库',
                        key: 'schemaName'
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
                                        type: 'primary',
                                        size: 'small'
                                    },
                                    style: {
                                        marginRight: '5px'
                                    },
                                    on: {
                                        click: () => {
                                            this.$router.push({path:"/environment/environment-db-info",query:{id:params.row.id}})                                        
                                        }
                                    }
                                }, '编辑'),
                                h('Button', {
                                    props: {
                                        type: 'warning',
                                        size: 'small'
                                    },
                                    style: {
                                        marginRight: '5px'
                                    },
                                    on: {
                                        click: () => {
                                            this.synchronizeDatabase(params.row.id)
                                        }
                                    }
                                }, '同步'),
                                h('Button', {
                                    props: {
                                        type: 'info',
                                        size: 'small'
                                    },
                                    style: {
                                        marginRight: '5px'
                                    },
                                    on: {
                                        click: () => {
                                            this.$router.push({path:"/docs/dbdoc-list-info",query:{id:params.row.id}})
                                        }
                                    }
                                }, '查看文档'),
                                h('Button', {
                                    props: {
                                        type: 'error',
                                        size: 'small'
                                    },
                                    on: {
                                        click: () => {
                                            this.deleteDatabaseNet(params.row.id)
                                        }
                                    }
                                }, '删除')
                            ]);
                        }
                    }
            ],
            list:[],
            databaseDataModel:{
                    id: 0,
                    name: "",
                    host: "",
                    port: 3306,
                    username: "",
                    password: "",
                    schemaName: "",
                    // todo 从当前用户的数据读，先写死了
                    businessUnit: 2,
                    productUnit: 1,
            },
        };
    },
    methods: {
        initDatabaseDataModel() {
            this.databaseDataModel = {
                id: 0,
                name: "",
                host: "",
                port: 3306,
                username: "",
                password: "",
                schemaName: "",
                businessUnit: 2,
                productUnit: 1,

            };
        },
        getData () {
            this.getDatabaseList()
        },
        getDatabaseList() {
            // todo id写死了
            return axios.get("/v1/database/getDatabaseList",
            {"params":{"id": 2}}).then((res)=>{
                if(res.data.success){
                    this.list = res.data.message;
                    // return res
                }else{
                    this.$Message.error("失败")
                }
            }
            )
        },
        addDatabase(){
            this.initDatabaseDataModel()
            this.$Modal.confirm({
                onOk: () => {
                       this.addDatabaseNet();
                    },
                    render: (h) => {
                    return h('div',[
                        h('Input', {
                            props: {
                                value: this.databaseDataModel.name,
                                autofocus: true,
                                placeholder: '数据库名'
                            },
                            on: {
                                input: (val) => {
                                    this.databaseDataModel.name = val;
                                }
                            }
                        }),
                        h('Input', {
                            props: {
                                value: this.databaseDataModel.host,
                                autofocus: false,
                                placeholder: '主机名'
                            },
                            style: {
                                marginTop: '8px'
                            },
                            on: {
                                input: (val) => {
                                    this.databaseDataModel.host = val;
                                }
                            }
                        }),
                        h('Input', {
                            props: {
                                value: this.databaseDataModel.port,
                                autofocus: false,
                                placeholder: '端口号'
                            },
                            style: {
                                marginTop: '8px'
                            },
                            on: {
                                input: (val) => {
                                    this.databaseDataModel.port = val;
                                }
                            }
                        }),
                        h('Input', {
                            props: {
                                value: this.databaseDataModel.username,
                                autofocus: false,
                                placeholder: '用户名'
                            },
                            style: {
                                marginTop: '8px'
                            },
                            on: {
                                input: (val) => {
                                    this.databaseDataModel.username = val;
                                }
                            }
                        }),
                        h('Input', {
                            props: {
                                value: this.databaseDataModel.password,
                                autofocus: false,
                                placeholder: '密码'
                            },
                            style: {
                                marginTop: '8px'
                            },
                            on: {
                                input: (val) => {
                                    this.databaseDataModel.password = val;
                                }
                            }
                        }),
                        h('Input', {
                            props: {
                                value: this.databaseDataModel.schemaName,
                                autofocus: false,
                                placeholder: '数据库'
                            },
                            style: {
                                marginTop: '8px'
                            },
                            on: {
                                input: (val) => {
                                    this.databaseDataModel.schemaName = val;
                                }
                            }
                        }),
                        // todo 从model先读默认值
                        // h('Select', {
                        //     props: {
                        //         value: this.databaseDataModel.businessUnit,
                        //         placeholder: '事业线'
                        //     },
                        //     style: {
                        //         marginTop: '8px'
                        //     },
                        //     on: {
                        //         input: (val) => {
                        //             this.databaseDataModel.businessUnit = val;
                        //         }
                        //     }
                        // }),
                    ])
                }
            })
        },
        addDatabaseNet(){
            axios.post("/v1/database/addDatabase",
            this.databaseDataModel
            ).then((res)=>{
                if(res.data.success){
                    this.$Message.success("成功");
                    this.getData();

                }else{
                    this.$Message.error("失败")
                }
            }
            )
            this.initDatabaseDataModel()
        },
        deleteDatabaseNet(index){
            axios.post("/v1/database/deleteDatabase",
            {"id": index}
            ).then((res)=>{
                if(res.data.success){
                    this.$Message.success("成功");
                    this.getData();
                }else{
                    this.$Message.error("失败")
                }
            }
            )
        },
        editDatabaseNet(index){
            axios.post("/v1/database/editDatabase",
            this.databaseDataModel
            ).then((res)=>{
                if(res.data.success){
                    this.$Message.success("成功");
                    this.getData();
                }else{
                    this.$Message.error("失败")
                }
            }
            )
            this.initDatabaseDataModel()
        },
        getDatabaseInfoByIdNet(index){
            axios.get("/v1/database/getDatabaseInfoById",
            {"params":{"id": index}}
            ).then((res)=>{
                if(res.data.success){
                    this.$Message.success("成功");
                    this.databaseDataModel=res.data.message[0]
                    this.editDatabase()
                }else{
                    this.$Message.error("失败")
                }
            }
            )
        },
        editDatabase(){

        },
        synchronizeDatabase(index) {
            axios.get("/v1/table/isInitSynchronize",
            {"params":{"id": index}}
            ).then((res)=>{
                if(res.data.success){
                    // this.$Message.success("成功");
                    let tableCount = res.data.message[0]["tableCount"]
                    if(tableCount == 0) {
                        this.initSynchronizeDatabaseNet(index)
                    } else {
                        this.synchronizeDatabaseNet(index)
                    }
                }else{
                    this.$Message.error("失败")
                }
            }
            )
        },

        initSynchronizeDatabaseNet(index){
            axios.post("/v1/table/initSynchronizeDatabase",
            {"id":index}
            ).then((res)=>{
                if(res.data.success){
                    this.$Message.success("成功");
                }else{
                    this.$Message.error("失败")
                }
            }
            )
        },
        synchronizeDatabaseNet(index){
            axios.post("/v1/table/synchronizeDatabase",
            {"id":index}
            ).then((res)=>{
                if(res.data.success){
                    this.$Message.success("成功");
                }else{
                    this.$Message.error("失败")
                }
            }
            )
        },
        deleteDatabaseNet(index){
            axios.post("/v1/database/deleteDatabase",
            {"id": index}
            ).then((res)=>{
                if(res.data.success){
                    this.$Message.success("成功");
                    this.getData();
                }else{
                    this.$Message.error("失败")
                }
            }
            )
        },
    },
    created () {
        this.getData();
    }
};
</script>
