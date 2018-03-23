<style lang="less">
    @import '../../styles/common.less';
    @import './components/table.less';
</style>

<template>
    <div>
        <!-- <Row type="flex" class="height-100">
            <Col span="8">
                <i-button type="success" @click="addDatabase" style="margin-top-10">新建数据库</i-button>
            </Col>
        </Row> -->
        <Row class="margin-top-10">
            <Col>
                <!-- <Card> -->
                    <div class="edittable-table-height-con">
                        <Table border :columns="lsitColumns" :data="list" @on-row-click="onRowClick"></Table>
                    </div>
                <!-- </Card> -->
            </Col>
        </Row>
    </div>
</template>

<script>
import axios  from 'axios';
export default {
    name: 'dbdoc-list',
    data () {
        return {
            lsitColumns: [

                    {
                        title: '数据库',
                        width: 120,
                        key: 'name'
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
                                            this.initSynchronizeDatabaseNet(params.row.id)                                           
                                        }
                                    }
                                }, '初始化同步'),
                                h('Button', {
                                    props: {
                                        type: 'error',
                                        size: 'small'
                                    },
                                    on: {
                                        click: () => {
                                            this.SynchronizeDatabaseNet(params.row.id)
                                        }
                                    }
                                }, '同步')
                            ]);
                        }
                    }
            ],
            list:[],
            databaseDataModel:{
                    id: 0,
                    name: "",
            },
        };
    },
    methods: {
        onRowClick(rowData,index){
            console.log(rowData)
            this.$router.push({path:"/docs/dbdoc-list-info",query:{id:rowData.id}})
        },
        initDatabaseDataModel() {
            this.databaseDataModel = {
                id: 0,
                name: "",
            };
        },
        getData () {
                axios.get("/v1/database/getDatabaseList").then((res)=>{
                console.log(res)
                if(res.data.success){
                    this.list = res.data.message;
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
        SynchronizeDatabaseNet(index){
            axios.post("/v1/table/SynchronizeDatabase",
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
    },
    created () {
        this.getData();
    }
};
</script>
