# codeflix
Full Cycle – Codeflix


## Next steps

- [ ] Add repository for Category (concrete implementation)
- [x] Use Notification Pattern for validation
- [ ] Decouple validations from entity (serializers)
- [x] Add `CreateCategory` and `ListCategories` usecases
- [ ] Implement a HTTP endpoint to access use cases
  - [ ] Django or FastAPI? (FlaskAPI might be simpler for DDD / Clean Arch approach)


## Business questions
- [ ] Should I be able to change a `Category` that is not active?
- [ ] Confirm `Category.change_category` should update both `name` and `description`
- [ ] Should we allow the id to be provided when creating a `Category`?
  - [ ] If so, should we validate it? uuid
- [ ] Confirm CategoryCreation logic usecase vs entity (should usecase create an inactive category?)


## Technical questions
- [ ] Notification: Entity depending directly on it
  - [ ] Also, when should I throw the error? In the [customer](https://github.com/devfullcycle/fc-clean-architecture/blob/main/src/domain/customer/entity/customer.ts) it only throws in the constructor. The `chaneName` calls validate but does not raise any error. Should application do it?
- [ ] Testing category "validation" seems redundant – constructor, updating, etc.
- [ ] If I want ordering, should the repository or the usecase provide it? Both?
- [ ] Do I need a factory for `Category`?
- [ ] Why in the DDD course `ProductInterface` does NOT have methods such as `changeName`, `changePrice`?
- [ ] Implement a FakeRepository instead of using mocks?
- [ ] Logging: is it something to be injected in the `AbstractEntity`? Similar to how we depend on `Event` and `Notification`?
- [x] Category Validation: should it be separated from `Category`? Notification pattern?
- [x] Should I test `Category.validate` directly or through `Category.__init__` and `Category.change_category`?
  - See `test_category.py::TestValidate` for more details
