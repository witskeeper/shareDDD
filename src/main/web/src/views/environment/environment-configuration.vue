<style lang="less">
    @import '../../styles/common.less';
</style>

<template>
    <div>
        <Row type="flex" class="height-100">
            <Col span="8">
                <i-button type="success" @click="addProject" style="margin-top-10">添加环境</i-button>
            </Col>
        </Row>
        <Row class="margin-top-10">
            <Col>
                <Card>
                    <div>
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
                        title: '环境名称',
                        key: 'name'
                    },
                    {
                        title: '创建人',
                        key: 'create_username'
                    },
                    {
                        title: '编辑时间',
                        key: 'gmt_modify'
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
                    userId:0
            }
        };
    },
    methods: {
        onRowClick(rowData,index){
                console.log(rowData)
                this.$router.push({path:"/environment/environment-info",query:{environmentId:rowData.id}})
        },
        getData () {
                axios.get("http://localhost:8090/v1/project/getProjectList").then((res)=>{
                console.log(res)
                if(res.data.success){
                    this.list = res.data.message;
                }else{
                    this.$Message.error("获取数据失败")
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
                                placeholder: '环境名称'
                            },
                            on: {
                                input: (val) => {
                                    this.addProjectData.name = val;
                                }
                            }
                        }),
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
                userId:0
            };
        }
    },
    created () {
        this.getData();
    }
};
</script>
