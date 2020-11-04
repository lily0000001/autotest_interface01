create table case_interface(
  id int(3) NOT NULL AUTO_INCREMENT,
  name_interface varchar( 128) NOT NULL comment '接口名称',
  exe_level int(3) default null comment '执行优先级，0代表BVT',
  exe_mode varchar(4) default null comment '执行方式：post、get 默认是post',
  url_interface varchar (128) default null comment '接口地址：直接使用http开头的详细地址',
  header_interface text comment '接口请求头文件 有则使用，无则不用',
  params_interface varchar(256) default null comment '接口请求参数',
  result_interface text comment '接口返回结果',
  code_to_compare varchar(16) default null comment '待比较的code值，用户自定义比较值',
  code_actual varchar(16) default null comment '接口实际code返回值',
  code_expect varchar(16) default null comment '接口实际code返回值',
  result_code_compare int(2) default null comment 'code 比较结果，1-pass ，0-fail，2-无比较参数，3-比较出错，
  9-系统异常',
  case_stutus int(2) default '0' comment '用例状态，1-有效，0-无效',
  create_time timestamp null default current_timestamp comment '创建时间',
  update_time timestamp null default current_timestamp on update current_timestamp comment '更新时间',
  primary key(id)
)engine = InnoDB auto_increment=1 default charset=utf8 comment='接口用例表';