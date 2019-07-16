### 编写初衷（原因）

* 现有view中，为了重写response为自定的结构，编写了很多重复代码（DRF）
* 为了使接口默认的response的json结构符合现有自定义形式，但不影响现有的anxin
一期，二期的代码。
* 重写异常exception_handler使编写的业务代码更加简洁(Flat is better than nested.)

### 主要修改点
 * 默认response结构
 * put 方法修改 patch的实现，方便编写修改个别字段接口
 * 默认的exception_handler


###测试方法
```
url(r'^test/', include('anxin.utils.view.test', namespace='test'))
```
> 顶层的urls.py中添加测试用的router
