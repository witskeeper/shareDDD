<style lang="less">
    @import '../../styles/common.less';
    @import './components/table.less';
</style>

<template>
    <div>
        <Row type="flex" class="height-100">
            <Col span="8">
                <i-button type="success" @click="addProject" style="margin-top-10">新建项目</i-button>
                <i-button type="success">导入项目</i-button>
            </Col>
        </Row>
        <Row class="margin-top-10">
            <Col>
                <Card>
                    <div class="edittable-table-height-con">
                        <Table border :columns="lsitColumns" :data="list" @on-row-click="onRowClick"></Table>
                    </div>
                </Card>
            </Col>
        </Row>
    </div>
</template>

<script>
import axios  from 'axios';
export default {
    name: 'interface-manage',
    data () {
        return {
            lsitColumns: [
                    {
                        title: 'create_username',
                        key: 'create_username'
                    },
                    {
                        title: 'name',
                        key: 'name'
                    },
                    {
                        title: 'gmt_modify',
                        key: 'gmt_modify'
                    },
                    {
                        title: 'version',
                        key: 'version'
                    },
                    {
                        title: 'remarks',
                        key: 'remarks'
                    },
                    {
                        title: '操作',
                        key: 'action',
                        width: 150,
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
                                            this.show(params.index)
                                        }
                                    }
                                }, '编辑'),
                                h('Button', {
                                    props: {
                                        type: 'error',
                                        size: 'small'
                                    },
                                    on: {
                                        click: () => {
                                            this.remove(params.index)
                                        }
                                    }
                                }, '删除')
                            ]);
                        }
                    }
            ],
            list:[],
            addProjectData:{
                    name:"",
                    userName:"",
                    userId:0,
                    version:"",
                    remarks:""
            }
        };
    },
    methods: {
        onRowClick(rowData,index){
                console.log(rowData)
                this.$router.push({path:"/interface/interface-info",query:{projectId:rowData.id}})
        },
        getData () {
                axios.get("http://localhost:8090/v1/project/getProjectInfoByName?name=SchoolpalShow").then((res)=>{
                console.log(res)
                if(res.data.success){
                    this.list = res.data.message;
                }else{
                    this.$Message.error("失败")
                }
            }
            )
        },
        addProject(){
            this.$Modal.confirm({
                onOk: () => {
                       this.addProjectNet();
                    },
                    render: (h) => {
                    return h('div',[
                        h('Input', {
                            props: {
                                value: this.addProjectData.name,
                                autofocus: true,
                                placeholder: '项目名称'
                            },
                            on: {
                                input: (val) => {
                                    this.addProjectData.name = val;
                                }
                            }
                        }),
                        h('Input', {
                            props: {
                                value: this.addProjectData.version,
                                autofocus: false,
                                placeholder: '项目版本'
                            },
                            style: {
                                marginTop: '8px'
                            },
                            on: {
                                input: (val) => {
                                    this.addProjectData.version = val;
                                }
                            }
                        }),
                        h('Input', {
                            props: {
                                value: this.addProjectData.remarks,
                                autofocus: false,
                                placeholder: '项目描述'
                            },
                            style: {
                                marginTop: '8px'
                            },
                            on: {
                                input: (val) => {
                                    this.addProjectData.remarks = val;
                                }
                            }
                        })
                    ])
                }
            })
        },
        addProjectNet(){
            axios.post("http://localhost:8090/v1/project/addProject",
            this.addProjectData
            ).then((res)=>{
                //console.log(res)
                if(res.data.success){
                    this.$Message.success("成功");
                    this.getData();

                }else{
                    this.$Message.error("失败")
                }
            }
            )
            this.addProjectData = {
                name:"",
                userName:"",
                userId:0,
                version:"",
                remarks:""

            };
        }
    },
    created () {
        this.getData();
    }
};
</script>
