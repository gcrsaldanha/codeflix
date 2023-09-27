# codeflix
Full Cycle – Codeflix


## Next steps

- [ ] Use Notification Pattern for validation ("Validações e Acoplamento" Clean Architecture course)
- [ ] Add repository for Category
- [ ] Add 2 use cases: `CreateCategory` and `ListCategories`
- [ ] Implement a HTTP endpoint to access use cases
  - [ ] Django or FastAPI? (FlaskAPI might be simpler for DDD / Clean Arch approach)


## Business questions
- [ ] Should I be able to change a category that is not active?


## Technical questions
- [ ] Do I need a factory for `Category`?
- [ ] Category Validation: should it be separated from `Category`? Notification pattern?
- [ ] Logging: is it something to be injected in the `AbstractEntity`? Similar to how we inject `Event`
- [ ] Why in the DDD course `ProductInterface` does NOT have methods such as `changeName`, `changePrice`?
- [ ] Should I test `Category.validate` directly or through `Category.__init__` and `Category.change_category`?
  - See `test_category.py::TestValidate` for more details
