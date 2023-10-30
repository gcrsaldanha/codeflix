# codeflix
Full Cycle – Codeflix


## Next steps

- [x] Use Notification Pattern for validation
- [x] Add `CreateCategory` and `ListCategories` usecases
- [x] Add repository for Category (concrete implementation)
- [x] Add APIs
- [x] Add e2e tests (API level)
- [x] Pagination
- [x] Ordering
- [x] Filter
- [x] Add activate/deactivate APIs
- [x] Abstract ListCategoriesRequest – pagination, ordering, filtering
- [x] Abstract serializers to usecase + generics
- [x] Extend to other entities (Genre, CastMember )
- [x] See how dependency injection was being made in old codeflix project (queryset/repository)
- [x] How to organize Django + DDD?
- [ ] Search with Regex vs Filter
- [ ] Decouple validations from entity (serializers)
- [ ] Revisit Notification pattern (exceptions/errors)
- [ ] Use `result` library for operations


## Business questions
- [ ] Confirm Genre/Category relationship
- [ ] Review create genre with categories use case.
  - Should GenreRepository be aware of categories?
- [ ] What should happen if genre/category is deleted?
  - prevent deleting used Category, allow deleting Genre
- [ ] Updating a Genre –> should we allow updating the categories? Or should it be a separate add/remove category usecase?
- [ ] Review GenreRepository: TODO - relationship with GenreCategory (get_by_id)
- [ ] Fetching the related Category Ids should be in the repository or in the Django Model? 
- [x] If the client is responsible for checking for NotificationError, then if it forgets to check, we can create a "bad" entity? E.g.: set `name="""` then save it.
- [x] Should I be able to change a `Category` that is not active?
- [x] Confirm `Category.change_category` should update both `name` and `description`
- [x] Should we allow the id to be provided when creating a `Category`?
  - [x] If so, should we validate it? uuid
- [x] Confirm CategoryCreation logic usecase vs entity (should usecase create an inactive category?)
- [x] `Genre` has a list of `Categories` (one-to-many?) – thus, `Category` should have a `Genre` FK / external UUID?
- [x] What are the business rules for `Genre`? Are `Category` required?
- [x] What if user adds same category?
- [x] What if user tries to remove category not present? (I made this idempotent)


## Technical questions
- [x] Do I always call validate on every method that mutates my entity? See `add_category`
- [x] What should "page_size" return?
- [x] Review generics for UseCase/Input/Output, Generics
- [x] Abstracting Paginator logic
- [x] Passing Paginator/Sorting/Filtering to repository/database?
- [x] Dependency on django.settings
- [x] Is it a problem to have the attribute name hardcoded (e.g.: order_by = {"name": Order.ASC})
- [x] Implementing fake repository with ordering, etc.?
- [x] Do we need to implement ordering and filtering in the API level? E.g.: ?page=1&page_size=3&order=-name => {"name": Order.DESC}
- [x] Dependency on django.settings – centralize?
- [x] Review folder structure
- [x] Soft delete? – Nope.
- [x] Application layer instantiating DjangoRepsitory directly? – Gateway/Factory?
- [x] Review usecases
- [x] Review e2e flow + tests
  - [x] TestListCategoryView should use the Repository or the use case for setup?
- [x] Serializer and input/output of usecases
- [x] Should serialization of get / list be different? (maybe will need in future)
- [x] id vs UUID
  - [x] Should Django model have default PK? Or should we use provided UUID always (in domain layer)?
- [x] Folder structure – app/domain/infra for each domain? category > app, domain, infra; genre > app, domain, infra...
- [x] Repository implementation: return created model? E.g.: might have a new ID
- [x] Notification: Entity depending directly on it
  - [x] Also, when should I throw the error? In the [customer](https://github.com/devfullcycle/fc-clean-architecture/blob/main/src/domain/customer/entity/customer.ts) it only throws in the constructor. The `chaneName` calls validate but does not raise any error. Should application do it?
- [x] Testing category "validation" seems redundant – constructor, updating, etc.
- [x] If I want ordering, should the repository or the usecase provide it? Both?
- [x] Do I need a factory for `Category`?
- [x] Why in the DDD course `ProductInterface` does NOT have methods such as `changeName`, `changePrice`?
- [x] Implement a FakeRepository instead of using mocks?
- [x] Logging: is it something to be injected in the `AbstractEntity`? Similar to how we depend on `Event` and `Notification`?
- [x] Category Validation: should it be separated from `Category`? Notification pattern?
- [x] Should I test `Category.validate` directly or through `Category.__init__` and `Category.change_category`?
  - See `test_category.py::TestValidate` for more details
- [x] Where should Validator / UseCaseInterface live? In the domain layer? Similar to repository interface.


## Meeting 2023-10-17
- 





## References
- [ ] Monads: https://github.com/dbrattli/OSlash
- [ ] RxJS
