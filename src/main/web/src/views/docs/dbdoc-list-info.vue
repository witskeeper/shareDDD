<style lang="less">
@import "../../styles/common.less";
@import "./components/table.less";
</style>

<template>
    <div>
        <Row>
            <!-- <Card> -->
            
            <Col span="18">
                <div>
                    <!-- <Select v-model="searchSelect" multiple filterable remote :remote-method="remoteMethod2" :loading="loading2"> -->
                    <Select v-model="searchInput" placeholder="搜索表名(user) / 表字段(user.id)" 
                     filterable remote :remote-method="remoteSearch" :loading="selectIsLoading" clearable @on-change="selectChange">
                        <Option v-for="item in searchList" :value="item.id" :key="item.uid">{{item.eName}}</Option>
                    </Select>
                </div>
                <div>
                    <div style="font-size:25px">  {{tableDataModel.eName}}（<span v-if="cNameEditIsHide">{{tableDataModel.cName}}</span>
                    <Input  v-if="!cNameEditIsHide" v-model="tableDataModel.cName" icon="checkmark" 
                    style="width: 200px" @on-click="editTableCNameByName"></Input>）
                        <Button  v-if="cNameEditIsHide" type="ghost" shape="circle" icon="edit"  size="small" 
                        @click="ChangeEditTableShow"></Button></div>
                </div>
                <div class="margin-top-10">    
                    <Input v-model="tableDataModel.remark" type="textarea" :autosize="{minRows: 2,maxRows: 5}" 
                    placeholder="备注" @on-blur="editTableByNameNet"></Input>
                </div>
                
                <div class="edittable-table-height-con margin-top-10">
                    <can-edit-table border :columns-list="listColumn" v-model="listData"
                    :hover-show="true" :edit-incell="true" @on-cell-change="handleCellChange" ></can-edit-table>
                </div>
                
            </Col>
            <Col span="6" class="padding-left-10">
            <!-- <div class="margin-top-10">
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
                </div> -->
                <div class="">
                    <Card>
                        <p slot="title">
                            <Icon type="navicon-round"></Icon>
                            【{{groupRelation.dbName}}】文档目录
                        </p>
                        <Tree ref="tree" :data="groupRelation.groupInfo" @on-select-change="getTreeTableInfo"></Tree>
                        <!-- <Tabs type="card"> -->
                            <!-- <TabPane label="所有分类目录">
                                <div class="classification-con">
                                    <Tree :data="classificationList" @on-check-change="setClassificationInAll" show-checkbox></Tree>
                                </div>
                            </TabPane> -->
                            <!-- <TabPane label="常用目录">
                                <div class="classification-con">
                                    <CheckboxGroup v-model="offenUsedClassSelected" @on-change="setClassificationInOffen">
                                        <p v-for="item in offenUsedClass" :key="item.title">
                                            <Checkbox :label="item.title">{{ item.title }}</Checkbox>
                                        </p>
                                    </CheckboxGroup>
                                </div>
                            </TabPane> -->
                    </Card>
                </div>
                
            </Col>
        <!-- </Card> -->
        </Row>
    </div>
</template>

<script>
import canEditTable from "./components/canEditTable.vue";
import axios from "axios";
export default {
  name: "dbdoc-list-info",
  components: {
    canEditTable
  },
  data() {
    return {
      selectIsLoading: false,
      treeTableName: "",
      listColumn: [
        {
          title: "字段",
          width: 120,
          key: "eName"
        },
        {
          title: "类型",
          width: 120,
          key: "type"
        },
        {
          title: "备注",
          key: "remark",
          editable: true
        },
        {
          title: "是否废弃",
          width: 120,
          key: "is_discarded",
          editable: true
        }
        // {
        //     title: '操作',
        //     align: 'center',
        //     width: 200,
        //     key: 'handle',
        //     handle: ['edit', 'delete']
        // }
      ],
      listData: [],
      tableDataModel: {
        id: 0,
        eName: "",
        cName: "",
        type: "",
        remark: "",
        is_discarded: 0
      },
      groupRelation: {
        dbName: "",
        groupInfo: []
      },
      DBId: 0,
      cNameEditIsHide: true,
      searchInput: "",
      searchList: [],
      searchList1: []
    };
  },
  methods: {
    initColumnDataModel() {
      this.tableDataModel = {
        id: 0,
        eName: "",
        cName: "",
        type: "",
        remark: "",
        is_discarded: 0
      };
    },
    getData() {
      // console.log(this.$route)
      this.DBId = this.$route.query.id;
      this.isSearch=0;
      this.getTableGroupRelationListNet();
           setInterval(()=>{
              this.isSearch++;
          },500);
    },
    getTableGroupRelationListNet() {
      axios
        .get("/v1/database/getTableGroupRelationList", {
          params: { id: this.DBId }
        })
        .then(res => {
          if (res.data.success) {
            // debugger
            this.groupRelation = res.data.message;
            this.treeTableName = this.groupRelation.groupInfo[0].children[0].title;
            this.getColumnListByTableNameNet(this.treeTableName);
            this.getTableInfoByNameNet(this.treeTableName);
            console.log(this.groupRelation)
            // var id = this.groupRelation.groupInfo[0].children[0].id;
            // this.getColumnListByTableIdNet(id);
            // this.getTableInfoByIdNet(id);
          } else {
            this.$Message.error("失败");
          }
        });
    },
    getTreeTableInfo(selectedArray) {
      console.log(selectedArray[0].title);
      const isHasChildren = selectedArray[0].children;
      var id = 0
      // todo 根节点不要选中且没有事件
      if (Array.isArray(isHasChildren)) {
        selectedArray[0].selected = false;
      } else {
        // this.treeTableName = selectedArray[0].title;
        id = selectedArray[0].tableId;
        console.log(selectedArray[0])
        this.getColumnListByTableIdNet(id);
        this.getTableInfoByIdNet(id);
      }
    //   this.getColumnListByTableNameNet(this.treeTableName);
    //   this.getTableInfoByNameNet(this.treeTableName);
    },
    getColumnListByTableNameNet(tableName) {
      axios
        .post("/v1/table/getColumnListByTableName", {
          DBId: this.DBId,
          eName: tableName
        })
        .then(res => {
          if (res.data.success) {
            this.listData = res.data.message;
          } else {
            this.$Message.error("失败");
          }
        });
    },
    getTableInfoByNameNet(tableName) {
      axios
        .post("/v1/table/getTableInfoByName", {
          DBId: this.DBId,
          eName: tableName
        })
        .then(res => {
          if (res.data.success) {
            this.tableDataModel = res.data.message[0];
          } else {
            this.$Message.error("失败");
          }
        });
    },
    getColumnListByTableIdNet(tableId) {
      axios
        .get("/v1/table/getColumnListByTableId", {
          params: { id: tableId}
        })
        .then(res => {
          if (res.data.success) {
            this.listData = res.data.message;
          } else {
            this.$Message.error("失败");
          }
        });
    },
    getTableInfoByIdNet(tableId) {
      axios
        .get("/v1/table/getTableInfoById", {
          params: { id: tableId}
        })
        .then(res => {
          if (res.data.success) {
            this.tableDataModel = res.data.message[0];
          } else {
            this.$Message.error("失败");
          }
        });
    },
    handleCellChange(val, index, key) {
      if (key === "is_discarded") {
        this.editColumnDiscardByIdNet(
          val[index][key],
          parseInt(val[index]["id"]),
          key
        );
      } else if (key === "remark") {
        this.editColumnRemarkByIdNet(val[index][key], val[index]["id"], key);
      }
      this.$Message.success(
        "修改了第 " + (index + 1) + " 行列名为 " + key + " 的数据"
      );
    },
    editColumnRemarkByIdNet(val, index, key) {
      axios
        .post("/v1/table/editColumnRemarkById", {
          id: index,
          key: key,
          val: val
        })
        .then(res => {
          if (res.data.success) {
            this.$Message.success("成功");
          } else {
            this.$Message.error("失败");
          }
        });
    },
    editColumnDiscardByNameNet(val, index, key) {
      axios
        .post("/v1/table/editColumnDiscardById", {
          id: index,
          key: key,
          val: val
        })
        .then(res => {
          if (res.data.success) {
            this.$Message.success("成功");
          } else {
            this.$Message.error("失败");
          }
        });
    },
    editTableByNameNet() {
      console.log("a");
      axios.post("/v1/table/editTableByName", this.tableDataModel).then(res => {
        if (res.data.success) {
          this.$Message.success("成功");
        } else {
          this.$Message.error("失败");
        }
      });
    },
    editTableCNameByName() {
      this.ChangeEditTableShow();
      this.editTableByNameNet();
    },
    ChangeEditTableShow() {
      this.cNameEditIsHide = !this.cNameEditIsHide;
    },
    remoteSearch(query) {
      if(this.isSearch%3!=0){
        return;
      }
      var index = query.indexOf(".");
      var content = { DBId: this.DBId, content: query };
      if(content != "") {
        if (index > 0) {
          // table.column
          this.getSearchList(0, content);
        } else if (index == -1) {
          // table
          this.getSearchList(1, content);
        } else if (index == 0) {
          // .column
          this.getSearchList(2, content);
        }
      }
      
    },
    getSearchList(searchType, content) {
      if (searchType == 0) {
        // table.column
        this.selectIsLoading = true;
        axios.post("/v1/table/getSearchByTableColumn", content).then(res => {
          if (res.data.success) {
            this.$Message.success("成功");
            this.searchList = res.data.message;
            this.selectIsLoading = false;
          } else {
            this.$Message.error("失败");
          }
        });
      } else if (searchType == 1) {
        // table
        this.selectIsLoading = true;
        axios.post("/v1/table/getSearchByTable", content).then(res => {
          if (res.data.success) {
             this.$Message.success("成功");
            this.searchList = res.data.message;
            this.selectIsLoading = false;
          } else {
            this.$Message.error("失败");
          }
        });
      } else if (searchType == 2) {
        // .column
        this.selectIsLoading = true;
        axios.post("/v1/table/getSearchByColumn", content).then(res => {
            if (res.data.success) {
                this.$Message.success("成功");
                this.searchList = res.data.message;
                this.selectIsLoading = false;
            } else {
                this.$Message.error("失败");
            }
        });
      }
    },
    selectChange(val) {
        var id = val
        if(id > 0) {
          this.getColumnListByTableIdNet(id);
          this.getTableInfoByIdNet(id);
          this.changeTreeSelected(id)
        }
        
    },
    changeTreeSelected(id) {

this.groupRelation.groupInfo.forEach(grops =>{
  grops.children.forEach(item =>{
    if(item.id==id){
      this.$set(item,'selected',true);
    }else{
      this.$set(item,'selected',false);
    }
  })
})

        // var groups = this.groupRelation.groupInfo
        // var res = groups.map(item => {
        //     var flag = false
        //     var inTree = item.children
        //     inTree.map(inItem => {
        //         // 判断选中节点
        //         if(inItem.tableId == id) {
        //             inItem.selected = true
        //             // 展开选中节点的根目录
        //             flag = true
        //         }else {
        //             inItem.selected = false
        //         }
        //         return inTree
        //     })
        //     if(flag) {
        //         item.expand = true
        //     }
        //     // 要不要折叠之前的节点
        //     return item
        // });
        // // console.log("bbb")
        // this.groupRelation.groupInfo = res

// debugger
      // this.groupRelation.groupInfo.forEach(item1 =>{
      //   debugger
      //   console.log(item1)
      //   item1.children[0].selected=false;
      //   item1.children[1].selected=true;
      // })


    }
  },
  mounted() {
    // this.changeTreeSelected()
    // this.groupRelationList = this.groupRelation.groupRelationList
    // this.listData = getTreeTableInfo
    // this.getColumnListByTableNameNet(this.treeTableName)
    // this.getTableInfoByNameNet(this.treeTableName)
  },
  created() {
    this.getData();
  }
};
</script>
