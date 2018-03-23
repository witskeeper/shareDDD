<style lang="less">
    @import '../../styles/common.less';
    @import './components/table.less';
</style>

<template>
    <div>
        <Row type="flex" class="height-100">
            <Col span="8">
                <i-button type="success" @click="addProduct" style="margin-top-10">新建产品</i-button>
            </Col>
        </Row>
        <Row class="margin-top-10">
            <Col>
                <!-- <Card> -->
                    <div class="edittable-table-height-con">
                        <Table border :columns="listColumns" :data="list"></Table>
                    </div>
                <!-- </Card> -->
            </Col>
        </Row>
    </div>
</template>

<script>
import axios  from 'axios';
export default {
    name: 'business-product',
    data () {
        return {
            listColumns: [

                    {
                        title: '事业线',
                        key: 'businessUnit'
                    },
                    {
                        title: '业务',
                        key: 'productName'
                    },
                    {
                        title: '操作',
                        key: 'id',
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
                                            this.getProductInfoByIdNet(params.row.id)                                           
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
                                            this.deleteProductNet(params.row.id)
                                        }
                                    }
                                }, '删除')
                            ]);
                        }
                    }
            ],
            list:[],
            ProductDataModel:{
                    id: 0,
                    businessUnit: 0,
                    productName: "",
            },
        };
    },
    methods: {
        // onRowClick(rowData,index){
        //         console.log(rowData)
        //         this.$router.push({path:"/interface/interface-info",query:{projectId:rowData.id}})
        // },
        initProductDataModel() {
            this.ProductDataModel = {
                    id: 0,
                    businessUnit: 0,
                    productName: "",

            };
        },
        getData () {
                axios.get("/v1/product/getProductList").then((res)=>{
                console.log(res)
                if(res.data.success){
                    this.list = res.data.message;
                }else{
                    this.$Message.error("失败")
                }
            }
            )
        },
        addProduct(){
            this.initProductDataModel()
            this.$Modal.confirm({
                onOk: () => {
                       this.addProductNet();
                    },
                    render: (h) => {
                    return h('div',[
                        h('Select', {
                            props: {
                                value: '', 
                                placeholder: '请选择事业线名'
                            },
                            on: {
                                change: (val) => {
                                    console.log(val)
                                    this.ProductDataModel.businessUnit = 2
                                }
                            }
                            },[
                            h('Option', {props: {value: 'IBU', key:1}}),
                            h('Option', {props: {value: 'TBU', key:2}}),
                            h('Option', {props: {value: 'NBU', key:3}}),
                        ]),
                        h('Input', {
                            props: {
                                value: this.ProductDataModel.productName,
                                autofocus: false,
                                placeholder: '业务名'
                            },
                            style: {
                                marginTop: '8px'
                            },
                            on: {
                                input: (val) => {
                                    this.ProductDataModel.productName = val;
                                }
                            }
                        }),
                    ])
                }
            })
        },
        addProductNet(){
            axios.post("/v1/product/addProduct",
            this.ProductDataModel
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
            this.initProductDataModel()
        },
        deleteProductNet(index){
            axios.post("/v1/product/deleteProduct",
            {"dababaseId": index}
            ).then((res)=>{
                //console.log(res)
                if(res.data.success){
                    this.$Message.success("成功");
                    this.getData();
                    // this.list.splice(index,1);

                }else{
                    this.$Message.error("失败")
                }
            }
            )
        },
        editProductNet(index){
            axios.post("/v1/product/editProduct",
            this.ProductDataModel
            ).then((res)=>{
                //console.log(res)
                if(res.data.success){
                    this.$Message.success("成功");
                    this.getData();
                    // this.list.splice(index,1);

                }else{
                    this.$Message.error("失败")
                }
            }
            )
            this.initProductDataModel()
        },
        getProductInfoByIdNet(index){
            axios.get("/v1/product/getProductInfoById",
            {"params":{"id": index}}
            ).then((res)=>{
                //console.log(res)
                if(res.data.success){
                    this.$Message.success("成功");
                    this.ProductDataModel=res.data.message[0]
                    this.editProduct()
                }else{
                    this.$Message.error("失败")
                }
            }
            )
        },
        editProduct(){
            this.$Modal.confirm({
                onOk: () => {
                       console.log(this.ProductDataModel)
                       this.editProductNet();
                    },
                    render: (h) => {
                    console.log(this.ProductDataModel)
                    return h('div',[
                        h('Select', {
                            props: {
                                value: 'NBU', 
                                placeholder: '请选择事业线名'
                            },
                            on: {
                                change: (val) => {
                                    console.log(val)
                                    this.ProductDataModel.businessUnit = 2
                                }
                            }
                            },[
                            h('Option', {props: {value: 'IBU', key:1}}),
                            h('Option', {props: {value: 'TBU', key:2}}),
                            h('Option', {props: {value: 'NBU', key:3}}),
                        ]),
                        h('Input', {
                            props: {
                                value: this.ProductDataModel.productName,
                                autofocus: false,
                                placeholder: '产品名'
                            },
                            style: {
                                marginTop: '8px'
                            },
                            on: {
                                input: (val) => {
                                    this.ProductDataModel.productName = val;
                                }
                            }
                        }),
                    ])
                }
            })
        },
    },
    
    created () {
        this.getData();
    }
};
</script>
