# codeflix
Full Cycle – Codeflix


## Next steps

- [x] Use Notification Pattern for validation
- [x] Add `CreateCategory` and `ListCategories` usecases
- [x] Add repository for Category (concrete implementation)
- [ ] Add APIs
- [ ] Add e2e tests (API level)
- [ ] Extend to other entities (Genre, CastMember ? )
- [ ] See how dependency injection was being made in old codeflix project (queryset/repository)
- [ ] Decouple validations from entity (serializers)
- [ ] Revisit inheritance of Exception in Python
- [ ] How to organize Django + DDD?


## Business questions
- [ ] If the client is responsible for checking for NotificationError, then if it forgets to check, we can create a "bad" entity? E.g.: set `name="""` then save it.
- [x] Should I be able to change a `Category` that is not active?
- [x] Confirm `Category.change_category` should update both `name` and `description`
- [ ] Should we allow the id to be provided when creating a `Category`?
  - [ ] If so, should we validate it? uuid
- [x] Confirm CategoryCreation logic usecase vs entity (should usecase create an inactive category?)


## Technical questions
- [ ] Folder structure – app/domain/infra for each domain? category > app, domain, infra; genre > app, domain, infra...
- [ ] TestListCategoryView should use the Repository or the use case for setup?
- [ ] Repository implementation: return created model? E.g.: might have a new ID
- [ ] Should Django model have default PK? Or should we use provided UUID always (in domain layer)?
- [x] Notification: Entity depending directly on it
  - [x] Also, when should I throw the error? In the [customer](https://github.com/devfullcycle/fc-clean-architecture/blob/main/src/domain/customer/entity/customer.ts) it only throws in the constructor. The `chaneName` calls validate but does not raise any error. Should application do it?
- [x] Testing category "validation" seems redundant – constructor, updating, etc.
- [x] If I want ordering, should the repository or the usecase provide it? Both?
- [x] Do I need a factory for `Category`?
- [ ] Why in the DDD course `ProductInterface` does NOT have methods such as `changeName`, `changePrice`?
- [x] Implement a FakeRepository instead of using mocks?
- [ ] Logging: is it something to be injected in the `AbstractEntity`? Similar to how we depend on `Event` and `Notification`?
- [x] Category Validation: should it be separated from `Category`? Notification pattern?
- [x] Should I test `Category.validate` directly or through `Category.__init__` and `Category.change_category`?
  - See `test_category.py::TestValidate` for more details
- [ ] Where should Validator / UseCaseInterface live? In the domain layer? Similar to repository interface.


Erro no dominio: 500
fora do dominio 422/400
