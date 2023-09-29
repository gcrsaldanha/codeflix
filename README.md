# codeflix
Full Cycle – Codeflix


## Next steps

- [x] Add repository for Category
- [x] Add `CreateCategory` and `ListCategories` usecases
- [ ] Implement a HTTP endpoint to access use cases
  - [ ] Django or FastAPI? (FlaskAPI might be simpler for DDD / Clean Arch approach)
- [ ] Use Notification Pattern for validation ("Validações e Acoplamento" Clean Architecture course)


## Business questions
- [ ] Should I be able to change a `Category` that is not active?
- [ ] Confirm `Category.change_category` should update both `name` and `description`
- [ ] Should we allow the id to be provided when creating a `Category`?
  - [ ] If so, should we validate it? uuid
- [ ] Confirm CategoryCreation logic usecase vs entity (should usecase create an inactive category?)


## Technical questions
- [ ] Do I need a factory for `Category`?
- [ ] Implement a FakeRepository instead of using mocks?
- [ ] Logging: is it something to be injected in the `AbstractEntity`? Similar to how we inject `Event`
- [ ] Why in the DDD course `ProductInterface` does NOT have methods such as `changeName`, `changePrice`?
- [x] Category Validation: should it be separated from `Category`? Notification pattern?
- [x] Should I test `Category.validate` directly or through `Category.__init__` and `Category.change_category`?
  - See `test_category.py::TestValidate` for more details
