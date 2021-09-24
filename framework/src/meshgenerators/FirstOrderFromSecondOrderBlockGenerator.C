//* This file is part of the MOOSE framework
//* https://www.mooseframework.org
//*
//* All rights reserved, see COPYRIGHT for full restrictions
//* https://github.com/idaholab/moose/blob/master/COPYRIGHT
//*
//* Licensed under LGPL 2.1, please see LICENSE for details
//* https://www.gnu.org/licenses/lgpl-2.1.html

#include "FirstOrderFromSecondOrderBlockGenerator.h"
#include "InputParameters.h"
#include "MooseTypes.h"
#include "CastUniquePointer.h"
#include "MooseMeshUtils.h"

#include "libmesh/distributed_mesh.h"
#include "libmesh/elem.h"
#include "libmesh/remote_elem.h"

#include <set>
#include <typeinfo>

registerMooseObject("MooseApp", FirstOrderFromSecondOrderBlockGenerator);

defineLegacyParams(FirstOrderFromSecondOrderBlockGenerator);

InputParameters
FirstOrderFromSecondOrderBlockGenerator::validParams()
{
  InputParameters params = MeshGenerator::validParams();

  params.addRequiredParam<MeshGeneratorName>("input", "The mesh we want to modify");
  params.addParam<SubdomainID>("new_block_id", "The first order block id to create");
  params.addParam<SubdomainName>("new_block_name",
                                 "The first order block name to create (optional)");
  params.addRequiredParam<std::vector<SubdomainID>>(
      "second_order_block_ids", "The second order block id that first order block will be created from");

  params.addClassDescription("Creates a first order block of elements from the nodes of a second order block,"
      "effectively sub-dividing the second order elements (e.g. a QUAD9 element is split into 4 QUAD4 elements).");

  return params;
}

FirstOrderFromSecondOrderBlockGenerator::FirstOrderFromSecondOrderBlockGenerator(const InputParameters & parameters)
  : MeshGenerator(parameters),
    _input(getMesh("input")),
    _second_order_block_ids(getParam<std::vector<SubdomainID>>("second_order_block_ids"))
{
}

std::unique_ptr<MeshBase>
FirstOrderFromSecondOrderBlockGenerator::generate()
{
  std::unique_ptr<MeshBase> mesh = std::move(_input);

  // Generate a new block id if one isn't supplied.
  SubdomainID new_block_id;
  if (isParamValid("new_block_id"))
    new_block_id = getParam<SubdomainID>("new_block_id");
  else
  {
    std::set<SubdomainID> preexisting_subdomain_ids;
    mesh->subdomain_ids(preexisting_subdomain_ids);
    if (preexisting_subdomain_ids.empty())
      new_block_id = 0;
    else
    {
      const auto highest_subdomain_id =
          *std::max_element(preexisting_subdomain_ids.begin(), preexisting_subdomain_ids.end());
      mooseAssert(highest_subdomain_id < std::numeric_limits<SubdomainID>::max(),
                  "A SubdomainID with max possible value was found");
      new_block_id = highest_subdomain_id + 1;
    }
  }

  // Loop over all elements in mesh, skip if not in second order blocks
  for (auto & so_elem : mesh->element_ptr_range())
  {
    bool in_blocks = false;
    for (auto so_blk_id : _second_order_block_ids)
    {
      if (so_elem->subdomain_id() == so_blk_id)
      {
        // Element belongs to one of the specified second order blocks
        in_blocks = true;

        // Check that element is indeed second order
        if (so_elem->default_order() != SECOND)
          mooseError("Element: ", so_elem->id(), " on block: ", so_blk_id, " is not second order");

        // Check that element is a compatible type for splitting
        auto type = so_elem->type();
        if (type == QUAD9 || type == TRI6)
          break;
        else
          mooseError("Element type: ", so_elem->type(), " is not yet supported for first order subdivision.");
      }
    }
    if (!in_blocks)
      continue;

    // max_elem_id should be consistent across procs assuming we've prepared our mesh previously
    mooseAssert(mesh->is_prepared(),
                "We are assuming that the mesh has been prepared previously in order to avoid a "
                "communication to determine the max elem id");

    // Build first order elements









  }

  // Assign block name, if provided
  if (isParamValid("new_block_name"))
    mesh->subdomain_name(new_block_id) = getParam<SubdomainName>("new_block_name");

  const bool skip_partitioning_old = mesh->skip_partitioning();
  mesh->skip_partitioning(true);
  mesh->prepare_for_use();
  mesh->skip_partitioning(skip_partitioning_old);

  return mesh;
}






  //
  // // Making an important assumption that at least our boundary elements are the same on all
  // // processes even in distributed mesh mode (this is reliant on the correct ghosting functors
  // // existing on the mesh)
  // for (MooseIndex(element_sides_on_boundary) i = 0; i < element_sides_on_boundary.size(); ++i)
  // {
  //   Elem * elem = element_sides_on_boundary[i].elem;
  //
  //   unsigned int side = element_sides_on_boundary[i].side;
  //
  //   // Build a non-proxy element from this side.
  //   std::unique_ptr<Elem> side_elem(elem->build_side_ptr(side, /*proxy=*/false));
  //
  //   // The side will be added with the same processor id as the parent.
  //   side_elem->processor_id() = elem->processor_id();
  //
  //   // Add subdomain ID
  //   side_elem->subdomain_id() = new_block_id;
  //
  //   // Also assign the side's interior parent, so it is always
  //   // easy to figure out the Elem we came from.
  //   side_elem->set_interior_parent(elem);
  //
  //   // Add id
  //   side_elem->set_id(max_elem_id + i);
  //   side_elem->set_unique_id(max_unique_id + i);
  //
  //   // Finally, add the lower-dimensional element to the Mesh.
  //   mesh->add_elem(side_elem.release());
  // };
